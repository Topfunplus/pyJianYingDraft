import { app, BrowserWindow, Menu, dialog, shell, ipcMain } from 'electron';
import { autoUpdater } from 'electron-updater';
import * as path from 'path';
import * as fs from 'fs';

class App {
  private mainWindow: BrowserWindow | null = null;
  private isDev = process.env.NODE_ENV === 'development';

  constructor() {
    this.initApp();
  }

  private initApp() {
    app.whenReady().then(() => {
      this.createWindow();
      this.setupMenu();
      this.setupIPC();
      
      if (!this.isDev) {
        autoUpdater.checkForUpdatesAndNotify();
      }
    });

    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        app.quit();
      }
    });

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        this.createWindow();
      }
    });
  }

  private createWindow() {
    this.mainWindow = new BrowserWindow({
      width: 1400,
      height: 900,
      minWidth: 1200,
      minHeight: 700,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload.js'),
        webSecurity: false // 允许跨域请求API
      },
      icon: path.join(__dirname, '../../assets/icon.png'),
      titleBarStyle: 'default',
      show: false
    });

    // 窗口准备好后显示
    this.mainWindow.once('ready-to-show', () => {
      this.mainWindow?.show();
      
      if (this.isDev) {
        this.mainWindow?.webContents.openDevTools();
      }
    });

    // 加载应用
    if (this.isDev) {
      this.mainWindow.loadURL('http://localhost:5173');
    } else {
      this.mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
    }

    // 处理外部链接
    this.mainWindow.webContents.setWindowOpenHandler(({ url }) => {
      shell.openExternal(url);
      return { action: 'deny' };
    });
  }

  private setupMenu() {
    const template: Electron.MenuItemConstructorOptions[] = [
      {
        label: '文件',
        submenu: [
          {
            label: '新建项目',
            accelerator: 'CmdOrCtrl+N',
            click: () => {
              this.mainWindow?.webContents.send('menu-new-project');
            }
          },
          {
            label: '打开项目',
            accelerator: 'CmdOrCtrl+O',
            click: async () => {
              const result = await dialog.showOpenDialog(this.mainWindow!, {
                properties: ['openDirectory'],
                title: '选择项目目录'
              });
              
              if (!result.canceled) {
                this.mainWindow?.webContents.send('menu-open-project', result.filePaths[0]);
              }
            }
          },
          { type: 'separator' },
          {
            label: '退出',
            accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
            click: () => {
              app.quit();
            }
          }
        ]
      },
      {
        label: '编辑',
        submenu: [
          { label: '撤销', accelerator: 'CmdOrCtrl+Z', role: 'undo' },
          { label: '重做', accelerator: 'Shift+CmdOrCtrl+Z', role: 'redo' },
          { type: 'separator' },
          { label: '剪切', accelerator: 'CmdOrCtrl+X', role: 'cut' },
          { label: '复制', accelerator: 'CmdOrCtrl+C', role: 'copy' },
          { label: '粘贴', accelerator: 'CmdOrCtrl+V', role: 'paste' }
        ]
      },
      {
        label: '视图',
        submenu: [
          { label: '重新加载', accelerator: 'CmdOrCtrl+R', role: 'reload' },
          { label: '强制重新加载', accelerator: 'CmdOrCtrl+Shift+R', role: 'forceReload' },
          { label: '开发者工具', accelerator: 'F12', role: 'toggleDevTools' },
          { type: 'separator' },
          { label: '实际大小', accelerator: 'CmdOrCtrl+0', role: 'resetZoom' },
          { label: '放大', accelerator: 'CmdOrCtrl+Plus', role: 'zoomIn' },
          { label: '缩小', accelerator: 'CmdOrCtrl+-', role: 'zoomOut' },
          { type: 'separator' },
          { label: '全屏', accelerator: 'F11', role: 'togglefullscreen' }
        ]
      },
      {
        label: '帮助',
        submenu: [
          {
            label: '关于',
            click: () => {
              dialog.showMessageBox(this.mainWindow!, {
                type: 'info',
                title: '关于剪映助手',
                message: '剪映草稿自动化桌面应用',
                detail: 'version 1.0.0\n\n一键生成剪映项目文件和素材包'
              });
            }
          },
          {
            label: '用户手册',
            click: () => {
              shell.openExternal('https://github.com/your-repo/jianying-draft-desktop');
            }
          }
        ]
      }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
  }

  private setupIPC() {
    // 选择目录
    ipcMain.handle('select-directory', async () => {
      const result = await dialog.showOpenDialog(this.mainWindow!, {
        properties: ['openDirectory'],
        title: '选择保存目录'
      });
      
      return result.canceled ? null : result.filePaths[0];
    });

    // 保存文件
    ipcMain.handle('save-file', async (_, filename: string, content: string) => {
      const result = await dialog.showSaveDialog(this.mainWindow!, {
        title: '保存文件',
        defaultPath: filename,
        filters: [
          { name: 'JSON Files', extensions: ['json'] },
          { name: 'All Files', extensions: ['*'] }
        ]
      });

      if (!result.canceled && result.filePath) {
        try {
          fs.writeFileSync(result.filePath, content, 'utf8');
          return { success: true, path: result.filePath };
        } catch (error) {
          return { success: false, error: (error as Error).message };
        }
      }

      return { success: false, error: '用户取消保存' };
    });

    // 检查目录是否存在
    ipcMain.handle('check-directory', async (_, dirPath: string) => {
      try {
        const stats = fs.statSync(dirPath);
        return stats.isDirectory();
      } catch {
        return false;
      }
    });

    // 创建目录
    ipcMain.handle('create-directory', async (_, dirPath: string) => {
      try {
        fs.mkdirSync(dirPath, { recursive: true });
        return { success: true };
      } catch (error) {
        return { success: false, error: (error as Error).message };
      }
    });
  }
}

new App();
