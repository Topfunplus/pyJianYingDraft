import React, { useState } from "react";
import {
  Layout as AntLayout,
  Menu,
  theme,
  Typography,
  Avatar,
  Space,
} from "antd";
import { useNavigate, useLocation } from "react-router-dom";
import {
  DashboardOutlined,
  ProjectOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UserOutlined,
} from "@ant-design/icons";
import { Film } from "lucide-react";
import { usePermissions } from "@/contexts/PermissionContext";
import UserProfile from "./UserProfile";

const { Header, Sider, Content } = AntLayout;
const { Title, Text } = Typography;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  // 获取权限信息
  const { hasPermission } = usePermissions();
  // 基础菜单项
  const baseMenuItems = [
    {
      key: "/",
      icon: <DashboardOutlined />,
      label: "仪表盘",
    },
    {
      key: "/create",
      icon: <ProjectOutlined />,
      label: "开始创作",
    },
    {
      key: "/projects",
      icon: <ProjectOutlined />,
      label: "项目管理",
    },
  ];
  // 管理员菜单项
  const adminMenuItems = [
    {
      key: "/users",
      icon: <UserOutlined />,
      label: "用户管理",
      requiresPermission: "can_manage_users" as const,
    },
  ];

  // 根据权限过滤菜单项
  const getFilteredMenuItems = () => {
    const menuItems = [...baseMenuItems];

    adminMenuItems.forEach((item) => {
      if (hasPermission(item.requiresPermission)) {
        menuItems.push({
          key: item.key,
          icon: item.icon,
          label: item.label,
        });
      }
    });

    return menuItems;
  };

  const menuItems = getFilteredMenuItems();

  return (
    <AntLayout style={{ minHeight: "100vh" }}>
      <Sider trigger={null} collapsible collapsed={collapsed} width={200}>
        <div
          style={{
            padding: "16px",
            textAlign: "center",
            borderBottom: "1px solid #f0f0f0",
            background: colorBgContainer,
          }}>
          <Space direction="vertical" size={4}>
            <Avatar
              size={collapsed ? 32 : 48}
              style={{ background: "#1890ff" }}
              icon={<Film size={collapsed ? 16 : 24} />}
            />
            {!collapsed && (
              <>
                <Title level={4} style={{ margin: 0, color: "#1890ff" }}>
                  剪映助手
                </Title>
                <Text type="secondary" style={{ fontSize: "12px" }}>
                  v1.0.0
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
          style={{ border: "none" }}
        />
      </Sider>
      <AntLayout>
        <Header
          style={{
            padding: "0 20px",
            background: colorBgContainer,
            borderBottom: "1px solid #f0f0f0",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}>
          <Space>
            {React.createElement(
              collapsed ? MenuUnfoldOutlined : MenuFoldOutlined,
              {
                className: "trigger",
                onClick: () => setCollapsed(!collapsed),
                style: { fontSize: "18px", cursor: "pointer" },
              }
            )}
          </Space>

          <UserProfile />
        </Header>
        <Content
          style={{
            margin: "24px",
            padding: "24px",
            background: colorBgContainer,
            borderRadius: "8px",
            minHeight: "calc(100vh - 112px)",
            overflow: "auto",
          }}>
          {children}
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;
