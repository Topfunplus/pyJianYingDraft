import React, { useState } from "react";
import {
  Row,
  Col,
  Card,
  Button,
  Table,
  Tag,
  Space,
  Typography,
  Modal,
  Form,
  Input,
  Switch,
  message,
  Popconfirm,
  Avatar,
  Tooltip,
  Drawer,
  Descriptions,
  Badge,
} from "antd";
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  UserOutlined,
  EyeOutlined,
  MailOutlined,
  CalendarOutlined,
} from "@ant-design/icons";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiService, User, CreateUserData, UpdateUserData } from "@/services/api";
import type { ColumnsType } from 'antd/es/table';

const { Title, Text } = Typography;

const UserManager: React.FC = () => {
  const queryClient = useQueryClient();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isViewDrawerVisible, setIsViewDrawerVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [viewingUser, setViewingUser] = useState<User | null>(null);
  const [form] = Form.useForm();

  // 获取用户列表
  const {
    data: usersData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["users"],
    queryFn: apiService.getUsers,
  });

  // 创建用户
  const createMutation = useMutation({
    mutationFn: apiService.createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
      message.success("用户创建成功");
      setIsModalVisible(false);
      form.resetFields();
    },
    onError: (error: any) => {
      message.error(`创建失败: ${error.message}`);
    },
  });

  // 更新用户
  const updateMutation = useMutation({
    mutationFn: ({ userId, userData }: { userId: number; userData: UpdateUserData }) =>
      apiService.updateUser(userId, userData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
      message.success("用户更新成功");
      setIsModalVisible(false);
      setEditingUser(null);
      form.resetFields();
    },
    onError: (error: any) => {
      message.error(`更新失败: ${error.message}`);
    },
  });

  // 删除用户
  const deleteMutation = useMutation({
    mutationFn: apiService.deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
      message.success("用户删除成功");
    },
    onError: (error: any) => {
      message.error(`删除失败: ${error.message}`);
    },
  });

  const handleCreate = () => {
    setEditingUser(null);
    form.resetFields();
    setIsModalVisible(true);
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    form.setFieldsValue({
      username: user.username,
      email: user.email,
      nickname: user.nickname,
      is_active: user.is_active,
    });
    setIsModalVisible(true);
  };

  const handleView = (user: User) => {
    setViewingUser(user);
    setIsViewDrawerVisible(true);
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      
      if (editingUser) {
        // 更新用户
        updateMutation.mutate({
          userId: editingUser.id,
          userData: values,
        });
      } else {
        // 创建用户
        createMutation.mutate(values);
      }
    } catch (error) {
      console.error("表单验证失败:", error);
    }
  };

  const handleDelete = (userId: number) => {
    deleteMutation.mutate(userId);
  };

  const handleStatusToggle = (user: User) => {
    updateMutation.mutate({
      userId: user.id,
      userData: { is_active: !user.is_active },
    });
  };

  const columns: ColumnsType<User> = [
    {
      title: '用户',
      key: 'user',
      render: (_, record) => (
        <Space>
          <Avatar
            size="small"
            style={{ backgroundColor: record.is_active ? '#87d068' : '#ff4d4f' }}
            icon={<UserOutlined />}
          />
          <div>
            <div style={{ fontWeight: 500 }}>{record.nickname || record.username}</div>
            <Text type="secondary" style={{ fontSize: '12px' }}>
              @{record.username}
            </Text>
          </div>
        </Space>
      ),
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email',
      render: (email) => email ? (
        <Space>
          <MailOutlined style={{ color: '#1890ff' }} />
          {email}
        </Space>
      ) : (
        <Text type="secondary">未设置</Text>
      ),
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (is_active, record) => (
        <Tooltip title="点击切换状态">
          <Tag
            color={is_active ? 'green' : 'red'}
            style={{ cursor: 'pointer' }}
            onClick={() => handleStatusToggle(record)}
          >
            {is_active ? '激活' : '禁用'}
          </Tag>
        </Tooltip>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (created_at) => (
        <Space>
          <CalendarOutlined style={{ color: '#666' }} />
          <Text style={{ fontSize: '12px' }}>
            {new Date(created_at).toLocaleString()}
          </Text>
        </Space>
      ),
    },
    {
      title: '操作',
      key: 'actions',
      render: (_, record) => (
        <Space size="small">
          <Tooltip title="查看详情">
            <Button
              type="text"
              size="small"
              icon={<EyeOutlined />}
              onClick={() => handleView(record)}
            />
          </Tooltip>
          <Tooltip title="编辑用户">
            <Button
              type="text"
              size="small"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
            />
          </Tooltip>
          <Tooltip title="删除用户">
            <Popconfirm
              title="确认删除"
              description="删除用户将同时删除其所有项目数据，此操作不可恢复。"
              onConfirm={() => handleDelete(record.id)}
              okText="确认删除"
              cancelText="取消"
              okType="danger"
            >
              <Button
                type="text"
                size="small"
                danger
                icon={<DeleteOutlined />}
                loading={deleteMutation.isPending}
              />
            </Popconfirm>
          </Tooltip>
        </Space>
      ),
    },
  ];

  const users = usersData?.data || [];
  const stats = usersData?.stats || {};

  return (
    <div>
      <div
        style={{
          marginBottom: "24px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div>
          <Title level={2}>
            <Space>
              <UserOutlined />
              用户管理
            </Space>
          </Title>
          <Text type="secondary">管理系统用户和权限</Text>
        </div>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleCreate}
          loading={createMutation.isPending}
        >
          添加用户
        </Button>
      </div>

      {/* 统计卡片 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={8}>
          <Card size="small">
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1890ff' }}>
                {users.length}
              </div>
              <div style={{ color: '#666', fontSize: '14px' }}>总用户数</div>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card size="small">
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#52c41a' }}>
                {users.filter(u => u.is_active).length}
              </div>
              <div style={{ color: '#666', fontSize: '14px' }}>活跃用户</div>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card size="small">
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#fa541c' }}>
                {users.filter(u => !u.is_active).length}
              </div>
              <div style={{ color: '#666', fontSize: '14px' }}>禁用用户</div>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 用户表格 */}
      <Card>
        <Table
          columns={columns}
          dataSource={users}
          rowKey="id"
          loading={isLoading}
          pagination={{
            total: users.length,
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) =>
              `第 ${range[0]}-${range[1]} 条，共 ${total} 条`,
          }}
        />
      </Card>

      {/* 创建/编辑用户模态框 */}
      <Modal
        title={editingUser ? "编辑用户" : "添加用户"}
        open={isModalVisible}
        onOk={handleSubmit}
        onCancel={() => {
          setIsModalVisible(false);
          setEditingUser(null);
          form.resetFields();
        }}
        confirmLoading={createMutation.isPending || updateMutation.isPending}
        okText={editingUser ? "更新" : "创建"}
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="username"
            label="用户名"
            rules={[
              { required: true, message: "请输入用户名" },
              { min: 3, message: "用户名至少3个字符" },
              { max: 20, message: "用户名最多20个字符" },
              { pattern: /^[a-zA-Z0-9_]+$/, message: "只能包含字母、数字和下划线" },
            ]}
          >
            <Input placeholder="输入用户名" />
          </Form.Item>

          <Form.Item
            name="nickname"
            label="昵称"
            rules={[{ max: 50, message: "昵称最多50个字符" }]}
          >
            <Input placeholder="输入昵称（可选）" />
          </Form.Item>

          <Form.Item
            name="email"
            label="邮箱"
            rules={[
              { type: "email", message: "请输入有效的邮箱地址" },
              { max: 100, message: "邮箱地址最多100个字符" },
            ]}
          >
            <Input placeholder="输入邮箱地址（可选）" />
          </Form.Item>

          <Form.Item
            name="is_active"
            label="用户状态"
            valuePropName="checked"
            initialValue={true}
          >
            <Switch
              checkedChildren="激活"
              unCheckedChildren="禁用"
              defaultChecked
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 用户详情抽屉 */}
      <Drawer
        title="用户详情"
        placement="right"
        width={480}
        open={isViewDrawerVisible}
        onClose={() => {
          setIsViewDrawerVisible(false);
          setViewingUser(null);
        }}
      >
        {viewingUser && (
          <div>
            <div style={{ textAlign: 'center', marginBottom: 24 }}>
              <Avatar
                size={80}
                style={{ backgroundColor: viewingUser.is_active ? '#87d068' : '#ff4d4f' }}
                icon={<UserOutlined />}
              />
              <div style={{ marginTop: 12 }}>
                <Title level={4} style={{ margin: 0 }}>
                  {viewingUser.nickname || viewingUser.username}
                </Title>
                <Text type="secondary">@{viewingUser.username}</Text>
                <div style={{ marginTop: 8 }}>
                  <Badge
                    status={viewingUser.is_active ? 'success' : 'error'}
                    text={viewingUser.is_active ? '账户正常' : '账户禁用'}
                  />
                </div>
              </div>
            </div>

            <Descriptions column={1} bordered size="small">
              <Descriptions.Item label="用户ID">
                {viewingUser.id}
              </Descriptions.Item>
              <Descriptions.Item label="用户名">
                {viewingUser.username}
              </Descriptions.Item>
              <Descriptions.Item label="昵称">
                {viewingUser.nickname || '未设置'}
              </Descriptions.Item>
              <Descriptions.Item label="邮箱">
                {viewingUser.email || '未设置'}
              </Descriptions.Item>
              <Descriptions.Item label="账户状态">
                <Tag color={viewingUser.is_active ? 'green' : 'red'}>
                  {viewingUser.is_active ? '激活' : '禁用'}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="创建时间">
                {new Date(viewingUser.created_at).toLocaleString()}
              </Descriptions.Item>
              <Descriptions.Item label="更新时间">
                {new Date(viewingUser.updated_at).toLocaleString()}
              </Descriptions.Item>
            </Descriptions>

            <div style={{ marginTop: 24 }}>
              <Space>
                <Button
                  type="primary"
                  icon={<EditOutlined />}
                  onClick={() => {
                    setIsViewDrawerVisible(false);
                    handleEdit(viewingUser);
                  }}
                >
                  编辑用户
                </Button>
                <Button
                  onClick={() => handleStatusToggle(viewingUser)}
                  loading={updateMutation.isPending}
                >
                  {viewingUser.is_active ? '禁用账户' : '激活账户'}
                </Button>
              </Space>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
};

export default UserManager;
