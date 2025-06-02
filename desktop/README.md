# 剪映助手 - 桌面版

基于 Electron + React + TypeScript 构建的剪映草稿自动化生成桌面应用。

## 功能特性

- 🖥️ **原生桌面体验** - 基于 Electron 的跨平台桌面应用
- 🎬 **项目创建** - 一键生成综合剪映项目
- 📁 **文件管理** - 集成文件选择器和目录管理
- 💾 **本地保存** - 直接保存到本地文件系统
- 🔔 **系统通知** - 操作完成后的系统级通知
- ⚡ **高性能** - Vite + React 18 的现代开发体验

## 开发环境设置

### 安装依赖
```bash
cd desktop
npm install
```

### 开发模式
```bash
npm run dev
```
这将同时启动主进程和渲染进程的开发服务器。

### 构建应用
```bash
npm run build
```

### 打包发布
```bash
npm run dist
```

## 项目结构

```
desktop/
├── src/
│   ├── main/           # 主进程代码
│   │   ├── main.ts     # 主进程入口
│   │   └── preload.ts  # 预加载脚本
│   └── renderer/       # 渲染进程代码
│       ├── components/ # React 组件
│       ├── pages/      # 页面组件
│       ├── services/   # API 服务
│       └── App.tsx     # 应用入口
├── assets/             # 应用资源
├── dist/              # 构建输出
└── release/           # 打包输出
```

## 与 Web 版的差异

### 增强功能
1. **文件系统访问** - 直接访问本地文件系统
2. **目录选择器** - 原生文件夹选择对话框
3. **菜单栏集成** - 原生应用菜单
4. **自动更新** - 支持应用自动更新
5. **系统通知** - 原生系统通知

### 架构优势
- 无需浏览器环境
- 更好的性能表现
- 完整的文件系统权限
- 更接近原生应用体验

## 开发指南

### 主进程开发
- 位于 `src/main/main.ts`
- 负责窗口管理、菜单、文件操作等
- 通过 IPC 与渲染进程通信

### 渲染进程开发
- 位于 `src/renderer/`
- 基于 React + TypeScript
- 通过 preload 脚本访问主进程 API

### IPC 通信
```typescript
// 渲染进程调用主进程
const result = await window.electronAPI.selectDirectory();

// 主进程向渲染进程发送事件
mainWindow.webContents.send('menu-new-project');
```

## 部署说明

### Windows
- 生成 `.exe` 安装包
- 支持 NSIS 安装器
- 自动创建桌面快捷方式

### macOS
- 生成 `.dmg` 安装包
- 应用签名和公证
- 支持 App Store 分发

### Linux
- 生成 `.AppImage` 或 `.deb` 包
- 支持多种 Linux 发行版

## 故障排除

### 常见问题
1. **模块找不到** - 检查依赖安装和路径配置
2. **构建失败** - 确保 TypeScript 配置正确
3. **IPC 通信问题** - 检查 preload 脚本和上下文隔离

### 开发工具
- 使用 `Ctrl+Shift+I` 打开开发者工具
- 主进程日志在终端查看
- 渲染进程日志在开发者工具查看
