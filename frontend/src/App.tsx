import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ConfigProvider, theme, App as AntApp } from "antd";
import zhCN from "antd/locale/zh_CN";
import Layout from "@/components/Layout";
import ProtectedRoute from "@/components/ProtectedRoute";
import Dashboard from "@/pages/Dashboard";
import CreateProject from "@/pages/CreateProject";
import ProjectManager from "@/pages/ProjectManager";
import UserManager from "@/pages/UserManager";
import Login from "@/pages/Login";
import ApiDocs from "@/pages/ApiDocs";
import ApiDocumentation from "@/pages/ApiDocumentation";
import { PermissionProvider } from "@/contexts/PermissionContext";
import "./App.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 2,
      staleTime: 5 * 60 * 1000, // 5分钟
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        locale={zhCN}
        theme={{
          algorithm: theme.defaultAlgorithm,
          token: {
            colorPrimary: "#1890ff",
            borderRadius: 8,
            colorBgContainer: "#ffffff",
          },
          components: {
            Layout: {
              siderBg: "#ffffff",
              headerBg: "#ffffff",
            },
          },
        }}>
        <AntApp>
          <PermissionProvider>
            <Router>
              <Routes>
                {/* 公开路由 */}
                <Route path="/login" element={<Login />} />
              
              {/* 受保护的路由 */}
              <Route path="/" element={
                <ProtectedRoute>
                  <Layout>
                    <Dashboard />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/create" element={
                <ProtectedRoute>
                  <Layout>
                    <CreateProject />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/projects" element={
                <ProtectedRoute>
                  <Layout>
                    <ProjectManager />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/users" element={
                <ProtectedRoute>
                  <Layout>
                    <UserManager />
                  </Layout>
                </ProtectedRoute>
              } />
                <Route path="/docs" element={
                <ProtectedRoute>
                  <Layout>
                    <ApiDocs />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/api-documentation" element={
                <ProtectedRoute>
                  <Layout>
                    <ApiDocumentation />
                  </Layout>
                </ProtectedRoute>
              } />
                {/* 重定向未匹配的路由 */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Router>
        </PermissionProvider>
        </AntApp>
      </ConfigProvider>
    </QueryClientProvider>
  );
};

export default App;
