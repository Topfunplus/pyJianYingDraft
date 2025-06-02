import React, { useState, useEffect } from 'react';
import { Layout as AntLayout, Menu, theme, Typography, Avatar, Space, Badge, Button } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  ProjectOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  NotificationOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import { Film, Cpu } from 'lucide-react';

const { Header, Sider, Content } = AntLayout;
const { Title, Text } = Typography;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [version, setVersion] = useState('1.0.0');
  const navigate = useNavigate();
  const location = useLocation();
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  useEffect(() => {
    // 设置菜单事件监听
    if (window.electronAPI) {
      const unsubscribeNew = window.electronAPI.onMenuNewProject(() => {
        navigate('/create');
      });

      const unsubscribeOpen = window.electronAPI.onMenuOpenProject((path: string) => {
        console.log('打开项目:', path);
        // 这里可以处理项目打开逻辑
      });

      return () => {
        unsubscribeNew();
        unsubscribeOpen();
      };
    }
  }, [navigate]);

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '仪表盘',
    },
    {
      key: '/create',
      icon: <ProjectOutlined />,
      label: '开始创作',
    },
  ];

  const handleNewProject = () => {
    navigate('/create');
  };

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider trigger={null} collapsible collapsed={collapsed} width={240}>
        <div style={{ 
          padding: '16px', 
          textAlign: 'center',
          borderBottom: '1px solid #f0f0f0',
          background: colorBgContainer 
        }}>
          <Space direction="vertical" size={4}>
            <Avatar 
              size={collapsed ? 32 : 48} 
              style={{ background: '#1890ff' }}
              icon={<Film size={collapsed ? 16 : 24} />}
            />
            {!collapsed && (
              <>
                <Title level={4} style={{ margin: 0, color: '#1890ff' }}>
                  剪映助手
                </Title>
                <Text type="secondary" style={{ fontSize: '12px' }}>
                  桌面版 v{version}
                </Text>
              </>
            )}
          </Space>
        </div>
        
        <Menu
          theme="light"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ border: 'none' }}
        />

        {/* 底部快捷操作 */}
        {!collapsed && (
          <div style={{ 
            position: 'absolute', 
            bottom: '20px', 
            left: '20px', 
            right: '20px' 
          }}>
            <Button 
              type="primary" 
              block 
              icon={<ProjectOutlined />}
              onClick={handleNewProject}
              style={{ marginBottom: '8px' }}
            >
              新建项目
            </Button>
          </div>
        )}
      </Sider>
      
      <AntLayout>
        <Header style={{ 
          padding: '0 24px', 
          background: colorBgContainer,
          borderBottom: '1px solid #f0f0f0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <Space>
            {React.createElement(
              collapsed ? MenuUnfoldOutlined : MenuFoldOutlined,
              {
                className: 'trigger',
                onClick: () => setCollapsed(!collapsed),
                style: { fontSize: '18px', cursor: 'pointer' },
              }
            )}
            <Title level={4} style={{ margin: 0 }}>
              剪映助手 - 桌面版
            </Title>
          </Space>
          
          <Space>
            <Badge count={0} size="small">
              <NotificationOutlined style={{ fontSize: '18px' }} />
            </Badge>
            <SettingOutlined style={{ fontSize: '18px', cursor: 'pointer' }} />
            <Avatar icon={<Cpu size={16} />} />
          </Space>
        </Header>
        
        <Content style={{ 
          margin: '24px', 
          padding: '24px', 
          background: colorBgContainer,
          borderRadius: '8px',
          minHeight: 'calc(100vh - 112px)',
          overflow: 'auto'
        }}>
          {children}
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;
