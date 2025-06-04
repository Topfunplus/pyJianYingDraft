import React, { createContext, useContext, ReactNode } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService, UserPermissions } from '@/services/api';

interface PermissionContextType {
  permissions: UserPermissions | null;
  hasPermission: (permission: keyof UserPermissions) => boolean;
  isLoading: boolean;
}

const PermissionContext = createContext<PermissionContextType | undefined>(undefined);

export const usePermissions = () => {
  const context = useContext(PermissionContext);
  if (context === undefined) {
    throw new Error('usePermissions must be used within a PermissionProvider');
  }
  return context;
};

interface PermissionProviderProps {
  children: ReactNode;
}

export const PermissionProvider: React.FC<PermissionProviderProps> = ({ children }) => {
  // 获取当前用户权限信息
  const { data: currentUser, isLoading } = useQuery({
    queryKey: ['current-user'],
    queryFn: apiService.getCurrentUser,
    enabled: apiService.isAuthenticated(),
    staleTime: 5 * 60 * 1000,
  });

  // 获取仪表盘数据中的权限信息作为备份
  const { data: dashboardData } = useQuery({
    queryKey: ['dashboard-data'],
    queryFn: apiService.getDashboardData,
    enabled: apiService.isAuthenticated(),
    staleTime: 5 * 60 * 1000,
  });
  // 从多个来源提取权限信息
  const getPermissions = (): UserPermissions | null => {
    // 1. 首先从用户资料中获取权限 (来自 /api/me)
    if (currentUser?.permissions) {
      return {
        can_manage_users: currentUser.permissions.can_manage_users || false,
        can_access_api_debug: currentUser.permissions.can_access_api_debug || false,
      };
    }

    // 2. 从仪表盘数据中获取权限
    if (dashboardData?.user_info?.permissions) {
      return {
        can_manage_users: dashboardData.user_info.permissions.can_manage_users || false,
        can_access_api_debug: dashboardData.user_info.permissions.can_access_api_debug || false,
      };
    }

    // 3. 如果都没有，返回默认权限（非管理员）
    return {
      can_manage_users: false,
      can_access_api_debug: false,
    };
  };

  const permissions = getPermissions();

  const hasPermission = (permission: keyof UserPermissions): boolean => {
    if (!permissions) return false;
    return permissions[permission] === true;
  };

  const value: PermissionContextType = {
    permissions,
    hasPermission,
    isLoading,
  };

  return (
    <PermissionContext.Provider value={value}>
      {children}
    </PermissionContext.Provider>
  );
};
