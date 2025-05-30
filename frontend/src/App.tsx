import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ConfigProvider, theme, App as AntApp } from "antd";
import zhCN from "antd/locale/zh_CN";
import Layout from "@/components/Layout";
import Dashboard from "@/pages/Dashboard";
import ApiTest from "@/pages/ApiTest";
import ProjectManager from "@/pages/ProjectManager";
import CreateProject from "@/pages/CreateProject";
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
          <Router>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/create" element={<CreateProject />} />
                <Route path="/api-test" element={<ApiTest />} />
                <Route path="/projects" element={<ProjectManager />} />
              </Routes>
            </Layout>
          </Router>
        </AntApp>
      </ConfigProvider>
    </QueryClientProvider>
  );
};

export default App;
