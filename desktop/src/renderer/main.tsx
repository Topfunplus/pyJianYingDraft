import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// 等待 DOM 加载完成
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// 桌面版特定的初始化
if (window.electronAPI) {
  console.log('🖥️ 桌面版应用已启动');
  
  // 可以在这里添加桌面版特定的初始化逻辑
  window.electronAPI.showNotification(
    '剪映助手', 
    '桌面版应用启动成功！'
  );
}
