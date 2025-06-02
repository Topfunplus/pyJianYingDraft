import { contextBridge, ipcRenderer, IpcRendererEvent } from 'electron';

// 暴露安全的API到渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 目录操作
  selectDirectory: () => ipcRenderer.invoke('select-directory'),
  checkDirectory: (path: string) => ipcRenderer.invoke('check-directory', path),
  createDirectory: (path: string) => ipcRenderer.invoke('create-directory', path),
  
  // 文件操作
  saveFile: (filename: string, content: string) => 
    ipcRenderer.invoke('save-file', filename, content),
  
  // 菜单事件监听 - 修复参数类型
  onMenuNewProject: (callback: () => void) => {
    const wrappedCallback = (event: IpcRendererEvent) => callback();
    ipcRenderer.on('menu-new-project', wrappedCallback);
    return () => ipcRenderer.removeListener('menu-new-project', wrappedCallback);
  },
  
  onMenuOpenProject: (callback: (path: string) => void) => {
    const wrappedCallback = (event: IpcRendererEvent, path: string) => callback(path);
    ipcRenderer.on('menu-open-project', wrappedCallback);
    return () => ipcRenderer.removeListener('menu-open-project', wrappedCallback);
  },
  
  // 应用信息
  getVersion: () => ipcRenderer.invoke('get-version'),
  getPlatform: () => process.platform,
  
  // 通知
  showNotification: (title: string, body: string) => {
    new Notification(title, { body });
  }
});

// 类型定义
declare global {
  interface Window {
    electronAPI: {
      selectDirectory: () => Promise<string | null>;
      checkDirectory: (path: string) => Promise<boolean>;
      createDirectory: (path: string) => Promise<{ success: boolean; error?: string }>;
      saveFile: (filename: string, content: string) => Promise<{ success: boolean; path?: string; error?: string }>;
      onMenuNewProject: (callback: () => void) => () => void;
      onMenuOpenProject: (callback: (path: string) => void) => () => void;
      getVersion: () => Promise<string>;
      getPlatform: () => string;
      showNotification: (title: string, body: string) => void;
    };
  }
}
