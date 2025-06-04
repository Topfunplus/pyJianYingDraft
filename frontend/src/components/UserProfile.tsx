import React, { useState } from 'react';
import { 
  Avatar, 
  Dropdown, 
  Space, 
  Typography, 
  Modal, 
  Form, 
  Input, 
  Button, 
  message,
  Descriptions,
  Tag
} from 'antd';
import { 
  UserOutlined, 
  LogoutOutlined, 
  EditOutlined,
  InfoCircleOutlined,
  LockOutlined
} from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService, User } from '@/services/api';
import { useNavigate } from 'react-router-dom';

const { Text } = Typography;

const UserProfile: React.FC = () => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [isProfileModalVisible, setIsProfileModalVisible] = useState(false);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [isChangePasswordVisible, setIsChangePasswordVisible] = useState(false);
  const [form] = Form.useForm();
  const [passwordForm] = Form.useForm();
  // 获取当前用户信息
  const { data: currentUser, isLoading } = useQuery<User>({
    queryKey: ['current-user'],
    queryFn: apiService.getCurrentUser,
    enabled: apiService.isAuthenticated(),
    staleTime: 5 * 60 * 1000,
  });

  // 登出mutation
  const logoutMutation = useMutation({
    mutationFn: apiService.logout,
    onSuccess: () => {
      queryClient.clear();
      message.success('已安全退出');
      navigate('/login');
    },
  });
  // 更新资料mutation
  const updateMutation = useMutation({
    mutationFn: apiService.updateProfile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['current-user'] });
      message.success('个人信息更新成功');
      setIsEditModalVisible(false);
    },
    onError: (error: any) => {
      const errorData = error.response?.data;
      
      if (errorData?.errors && typeof errorData.errors === 'object') {
        // 处理字段级错误
        const formFields: any[] = [];
        let hasFieldErrors = false;
        
        Object.keys(errorData.errors).forEach(fieldName => {
          const errors = errorData.errors[fieldName];
          
          if (Array.isArray(errors) && errors.length > 0) {
            formFields.push({
              name: fieldName,
              errors: errors
            });
            hasFieldErrors = true;
          }
        });
        
        // 设置表单字段错误
        if (hasFieldErrors) {
          form.setFields(formFields);
        }
        
        // 显示通用错误消息
        message.error(errorData.message || '更新失败');
      } else {
        // 其他类型的错误
        message.error(errorData?.message || '更新失败');
      }
    },
  });// 修改密码mutation
  const changePasswordMutation = useMutation({
    mutationFn: apiService.changePassword,
    onSuccess: () => {
      message.success('密码修改成功');
      setIsChangePasswordVisible(false);
      passwordForm.resetFields();
    },
    onError: (error: any) => {
      const errorData = error.response?.data;
      
      if (errorData?.errors && typeof errorData.errors === 'object') {
        // 后端字段到前端字段的映射
        const fieldMapping: { [key: string]: string } = {
          'old_password': 'oldPassword',
          'new_password': 'newPassword', 
          'confirm_password': 'confirmNewPassword'
        };
        
        // 处理字段级错误
        const formFields: any[] = [];
        let hasFieldErrors = false;
        
        Object.keys(errorData.errors).forEach(backendField => {
          const frontendField = fieldMapping[backendField] || backendField;
          const errors = errorData.errors[backendField];
          
          if (Array.isArray(errors) && errors.length > 0) {
            formFields.push({
              name: frontendField,
              errors: errors
            });
            hasFieldErrors = true;
          }
        });
        
        // 设置表单字段错误
        if (hasFieldErrors) {
          passwordForm.setFields(formFields);
        }
        
        // 显示通用错误消息
        message.error(errorData.message || '密码修改失败');
      } else {
        // 其他类型的错误
        message.error(errorData?.message || '修改密码失败');
      }
    },
  });

  const handleLogout = () => {
    Modal.confirm({
      title: '确认退出',
      content: '确定要退出登录吗？',
      onOk: () => logoutMutation.mutate(),
    });
  };
  const handleChangePassword = async () => {
    try {
      const values = await passwordForm.validateFields();
      changePasswordMutation.mutate({
        old_password: values.oldPassword,
        new_password: values.newPassword,
        confirm_password: values.confirmNewPassword,
      });
    } catch (error) {
      console.error('表单验证失败:', error);
    }
  };

  const handleViewProfile = () => {
    setIsProfileModalVisible(true);
  };
  const handleEditProfile = () => {
    if (currentUser) {
      form.setFieldsValue({
        nickname: currentUser.nickname,
        email: currentUser.email,
      });
      setIsEditModalVisible(true);
    }
  };
  const handleUpdateProfile = async () => {
    try {
      const values = await form.validateFields();
      if (currentUser) {
        updateMutation.mutate(values);
      }
    } catch (error) {
      console.error('表单验证失败:', error);
    }
  };

  const menuItems = [
    {
      key: 'profile',
      icon: <InfoCircleOutlined />,
      label: '个人信息',
      onClick: handleViewProfile,
    },
    {
      key: 'edit',
      icon: <EditOutlined />,
      label: '编辑资料',
      onClick: handleEditProfile,
    },
    {
      key: 'password',
      icon: <LockOutlined />,
      label: '修改密码',
      onClick: () => setIsChangePasswordVisible(true),
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      onClick: handleLogout,
    },
  ];

  if (!apiService.isAuthenticated()) {
    return (
      <Button type="primary" onClick={() => navigate('/login')}>
        登录
      </Button>
    );
  }

  if (isLoading) {
    return (
      <Space>
        <Avatar icon={<UserOutlined />} />
        <Text>加载中...</Text>
      </Space>
    );
  }
  if (!currentUser) {
    return (
      <Button type="primary" onClick={() => navigate('/login')}>
        登录
      </Button>
    );
  }

  // currentUser 直接是 User 对象，不需要 .data
  const user = currentUser;  return (
    <>
      <Dropdown menu={{ items: menuItems }} trigger={['click']} placement="bottomRight">
        <Space 
          style={{ 
            cursor: 'pointer', 
            padding: '4px 8px',
            borderRadius: '6px',
            transition: 'background-color 0.2s'
          }}
          size="small"
        >
          <Avatar
            size="small"
            style={{ backgroundColor: user.is_active ? '#87d068' : '#ff4d4f' }}
            icon={<UserOutlined />}
          />
          <div style={{ 
            textAlign: 'left',
            lineHeight: 1.2,
            minWidth: '80px'
          }}>
            <div style={{ 
              fontSize: '14px', 
              fontWeight: 500,
              color: '#262626',
              marginBottom: '2px',
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              maxWidth: '120px'
            }}>
              {user.nickname || user.username}
            </div>
            <div style={{ 
              fontSize: '12px', 
              color: '#8c8c8c',
              lineHeight: 1
            }}>
              {user.is_active ? '在线' : '离线'}
            </div>
          </div>
        </Space>
      </Dropdown>

      {/* 个人信息查看模态框 */}
      <Modal
        title="个人信息"
        open={isProfileModalVisible}
        onCancel={() => setIsProfileModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setIsProfileModalVisible(false)}>
            关闭
          </Button>,
          <Button key="edit" type="primary" onClick={handleEditProfile}>
            编辑资料
          </Button>,
        ]}
      >
        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          <Avatar
            size={80}
            style={{ backgroundColor: user.is_active ? '#87d068' : '#ff4d4f' }}
            icon={<UserOutlined />}
          />
          <div style={{ marginTop: 12 }}>
            <div style={{ fontSize: '18px', fontWeight: 500 }}>
              {user.nickname || user.username}
            </div>
            <Text type="secondary">@{user.username}</Text>
            <div style={{ marginTop: 8 }}>
              <Tag color={user.is_active ? 'green' : 'red'}>
                {user.is_active ? '账户正常' : '账户禁用'}
              </Tag>
            </div>
          </div>
        </div>

        <Descriptions column={1} bordered size="small">
          <Descriptions.Item label="用户ID">{user.id}</Descriptions.Item>
          <Descriptions.Item label="用户名">{user.username}</Descriptions.Item>
          <Descriptions.Item label="昵称">
            {user.nickname || '未设置'}
          </Descriptions.Item>
          <Descriptions.Item label="邮箱">
            {user.email || '未设置'}
          </Descriptions.Item>
          <Descriptions.Item label="注册时间">
            {new Date(user.created_at).toLocaleString()}
          </Descriptions.Item>
          <Descriptions.Item label="最后更新">
            {new Date(user.updated_at).toLocaleString()}
          </Descriptions.Item>
        </Descriptions>
      </Modal>

      {/* 编辑资料模态框 */}
      <Modal
        title="编辑个人资料"
        open={isEditModalVisible}
        onOk={handleUpdateProfile}
        onCancel={() => {
          setIsEditModalVisible(false);
          form.resetFields();
        }}
        confirmLoading={updateMutation.isPending}
        okText="保存"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="nickname"
            label="昵称"
            rules={[{ max: 50, message: "昵称最多50个字符" }]}
          >
            <Input placeholder="输入昵称" />
          </Form.Item>

          <Form.Item
            name="email"
            label="邮箱"
            rules={[
              { type: "email", message: "请输入有效的邮箱地址" },
              { max: 100, message: "邮箱地址最多100个字符" },
            ]}
          >
            <Input placeholder="输入邮箱地址" />
          </Form.Item>
        </Form>
      </Modal>

      {/* 修改密码模态框 */}
      <Modal
        title="修改密码"
        open={isChangePasswordVisible}
        onOk={handleChangePassword}
        onCancel={() => {
          setIsChangePasswordVisible(false);
          passwordForm.resetFields();
        }}
        confirmLoading={changePasswordMutation.isPending}
        okText="确认修改"
        cancelText="取消"
      >
        <Form form={passwordForm} layout="vertical">
          <Form.Item
            name="oldPassword"
            label="当前密码"
            rules={[{ required: true, message: '请输入当前密码' }]}
          >
            <Input.Password placeholder="请输入当前密码" />
          </Form.Item>

          <Form.Item
            name="newPassword"
            label="新密码"
            rules={[
              { required: true, message: '请输入新密码' },
              { min: 6, message: '密码至少6个字符' }
            ]}
          >
            <Input.Password placeholder="请输入新密码" />
          </Form.Item>

          <Form.Item
            name="confirmNewPassword"
            label="确认新密码"
            dependencies={['newPassword']}
            rules={[
              { required: true, message: '请确认新密码' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('newPassword') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('两次输入的密码不一致'));
                },
              }),
            ]}
          >
            <Input.Password placeholder="请确认新密码" />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default UserProfile;
