import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { Spin } from 'antd';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '@/services/api';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const location = useLocation();

  // 检查是否有token
  if (!apiService.isAuthenticated()) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // 验证token有效性
  const { data: currentUser, isLoading, error } = useQuery({
    queryKey: ['current-user'],
    queryFn: apiService.getCurrentUser,
    retry: false,
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        <Spin size="large" />
      </div>
    );
  }
  if (error || !currentUser) {
    // Token无效，清除并重定向到登录页
    console.log('用户认证失败，清除token并重定向到登录页');
    console.error('认证错误:', error);
    apiService.clearToken();
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
