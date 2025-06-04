import React, { useState } from 'react';
import { Form, Input, Button, Card, message, Typography, Space, Tabs } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { apiService, LoginData, RegisterData } from '@/services/api';
import { Film } from 'lucide-react';
const { Title, Text, Link } = Typography;

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('login');
  const [loginForm] = Form.useForm();
  const [registerForm] = Form.useForm();  // 登录mutation
  const loginMutation = useMutation({
    mutationFn: apiService.login,
    onSuccess: (data) => {
      console.log('登录响应数据:', data);
      if (data.success) {
        message.success('登录成功，欢迎回来！');
        navigate('/', { replace: true });
      } else {
        message.error(data.message || '登录失败，请检查用户名和密码');
      }
    },
    onError: (error: any) => {
      console.error('登录错误详情:', error);
      console.error('错误响应:', error.response);
      
      let errorMessage = '登录失败';
      
      if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      message.error(`登录失败: ${errorMessage}`);
    },
  });

  // 注册mutation
  const registerMutation = useMutation({
    mutationFn: apiService.register,
    onSuccess: (data) => {
      console.log('注册响应数据:', data);
      if (data.success) {
        message.success('注册成功，欢迎使用剪映助手！');
        // 注册成功后跳转到dashboard（根路径）
        navigate('/', { replace: true });
      } else {
        message.error(data.message || '注册失败，请重试');
      }
    },
    onError: (error: any) => {
      console.error('注册错误详情:', error);
      console.error('错误响应:', error.response);
      
      let errorMessage = '注册失败';
      
      if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      // 如果是验证错误，显示具体的字段错误
      if (error.response?.data?.errors) {
        const errors = error.response.data.errors;
        if (Array.isArray(errors)) {
          errorMessage = errors.join(', ');
        } else if (typeof errors === 'object') {
          errorMessage = Object.values(errors).flat().join(', ');
        }
      }
      
      message.error(`注册失败: ${errorMessage}`);
    },
    });

  const handleLogin = async (values: LoginData) => {
    loginMutation.mutate(values);
  };
  const handleRegister = async (values: any) => {
    // 清理undefined值，只发送有值的字段
    const cleanData: any = {
      username: values.username,
      password: values.password,
    };
    
    if (values.confirmPassword) {
      cleanData.confirmPassword = values.confirmPassword;
    }
    if (values.nickname && values.nickname.trim()) {
      cleanData.nickname = values.nickname.trim();
    }
    if (values.email && values.email.trim()) {
      cleanData.email = values.email.trim();
    }
    
    console.log('注册数据:', cleanData);
    registerMutation.mutate(cleanData);
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px'
    }}>
      <Card style={{ width: '100%', maxWidth: '400px', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.1)' }}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <Space direction="vertical" size={8}>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
              <Film size={48} color="#1890ff" />
            </div>
            <Title level={2} style={{ margin: 0, color: '#1890ff' }}>
              剪映助手
            </Title>
            <Text type="secondary">欢迎使用剪映草稿自动化工具</Text>
          </Space>
        </div>

        <Tabs 
          activeKey={activeTab} 
          onChange={setActiveTab}
          centered
          items={[
            {
              key: 'login',
              label: '登录',
              children: (
                <Form
                  form={loginForm}
                  onFinish={handleLogin}
                  layout="vertical"
                  size="large"
                >
                  <Form.Item
                    name="username"
                    rules={[{ required: true, message: '请输入用户名' }]}
                  >
                    <Input
                      prefix={<UserOutlined />}
                      placeholder="用户名"
                    />
                  </Form.Item>

                  <Form.Item
                    name="password"
                    rules={[{ required: true, message: '请输入密码' }]}
                  >
                    <Input.Password
                      prefix={<LockOutlined />}
                      placeholder="密码"
                    />
                  </Form.Item>

                  <Form.Item>
                    <Button
                      type="primary"
                      htmlType="submit"
                      block
                      loading={loginMutation.isPending}
                    >
                      登录
                    </Button>
                  </Form.Item>

                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary">
                      还没有账号？
                      <Link onClick={() => setActiveTab('register')}>立即注册</Link>
                    </Text>
                  </div>
                </Form>
              )
            },
            {
              key: 'register',
              label: '注册',
              children: (
                <Form
                  form={registerForm}
                  onFinish={handleRegister}
                  layout="vertical"
                  size="large"
                >
                  <Form.Item
                    name="username"
                    rules={[
                      { required: true, message: '请输入用户名' },
                      { min: 3, max: 20, message: '用户名长度3-20个字符' },
                      { pattern: /^[a-zA-Z0-9_]+$/, message: '只能包含字母、数字和下划线' }
                    ]}
                  >
                    <Input
                      prefix={<UserOutlined />}
                      placeholder="用户名"
                    />
                  </Form.Item>

                  <Form.Item
                    name="nickname"
                    rules={[{ max: 50, message: '昵称最多50个字符' }]}
                  >
                    <Input
                      prefix={<UserOutlined />}
                      placeholder="昵称（可选）"
                    />
                  </Form.Item>

                  <Form.Item
                    name="email"
                    rules={[
                      { type: 'email', message: '请输入有效的邮箱地址' },
                      { max: 100, message: '邮箱地址最多100个字符' }
                    ]}
                  >
                    <Input
                      prefix={<MailOutlined />}
                      placeholder="邮箱（可选）"
                    />
                  </Form.Item>

                  <Form.Item
                    name="password"
                    rules={[
                      { required: true, message: '请输入密码' },
                      { min: 6, message: '密码至少6个字符' }
                    ]}
                  >
                    <Input.Password
                      prefix={<LockOutlined />}
                      placeholder="密码"
                    />
                  </Form.Item>

                  <Form.Item
                    name="confirmPassword"
                    dependencies={['password']}
                    rules={[
                      { required: true, message: '请确认密码' },
                      ({ getFieldValue }) => ({
                        validator(_, value) {
                          if (!value || getFieldValue('password') === value) {
                            return Promise.resolve();
                          }
                          return Promise.reject(new Error('两次输入的密码不一致'));
                        },
                      }),
                    ]}
                  >
                    <Input.Password
                      prefix={<LockOutlined />}
                      placeholder="确认密码"
                    />
                  </Form.Item>

                  <Form.Item>
                    <Button
                      type="primary"
                      htmlType="submit"
                      block
                      loading={registerMutation.isPending}
                    >
                      注册
                    </Button>
                  </Form.Item>

                  <div style={{ textAlign: 'center' }}>
                    <Text type="secondary">
                      已有账号？
                      <Link onClick={() => setActiveTab('login')}>立即登录</Link>
                    </Text>
                  </div>
                </Form>
              )
            }
          ]}
        />
      </Card>
    </div>
  );
};

export default Login;
