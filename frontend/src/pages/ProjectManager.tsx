import React, { useState } from "react";
import {
  Row,
  Col,
  Card,
  Button,
  List,
  Tag,
  Space,
  Typography,
  Modal,
  Form,
  Input,
  Select,
  message,
  Statistic,
  Alert,
} from "antd";
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  DownloadOutlined,
  EyeOutlined,
} from "@ant-design/icons";
import { ProjectOutlined } from "@ant-design/icons";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiService } from "@/services/api";

const { Title, Text } = Typography;
const { Option } = Select;

interface Project {
  id: string;
  name: string;
  type: string;
  status: "draft" | "completed" | "processing";
  createdAt: string;
  description: string;
}

const ProjectManager: React.FC = () => {
  const queryClient = useQueryClient();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  // 使用React Query获取项目数据
  const {
    data: projectsData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["projects"],
    queryFn: apiService.getProjects,
  });

  // 删除项目mutation
  const deleteMutation = useMutation({
    mutationFn: apiService.deleteProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      message.success("项目删除成功");
    },
    onError: (error: any) => {
      message.error(`删除失败: ${error.message}`);
    },
  });

  const handleCreateProject = () => {
    form.validateFields().then((values) => {
      const newProject: Project = {
        id: Date.now().toString(),
        ...values,
        status: "draft" as const,
        createdAt: new Date().toISOString().split("T")[0],
      };
      setProjects([...projects, newProject]);
      setIsModalVisible(false);
      form.resetFields();
      message.success("项目创建成功");
    });
  };

  const handleDeleteProject = (id: string) => {
    Modal.confirm({
      title: "确认删除",
      content: "确定要删除这个项目吗？",
      onOk: () => {
        deleteMutation.mutate(parseInt(id));
      },
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "green";
      case "processing":
        return "blue";
      case "draft":
        return "orange";
      default:
        return "default";
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "completed":
        return "已完成";
      case "processing":
        return "处理中";
      case "draft":
        return "草稿";
      default:
        return "未知";
    }
  };

  const projects = projectsData?.data || [];
  const stats = projectsData?.stats || {};

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
              <ProjectOutlined />
              项目管理
            </Space>
          </Title>
          <Text type="secondary">管理您的剪映草稿项目</Text>
        </div>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setIsModalVisible(true)}
        >
          创建新项目
        </Button>
      </div>

      {/* 添加统计卡片 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card size="small">
            <Statistic title="总项目数" value={stats.total_projects || 0} />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic title="已完成" value={stats.completed_projects || 0} />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic title="进行中" value={stats.processing_projects || 0} />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic title="草稿" value={stats.draft_projects || 0} />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card loading={isLoading}>
            {error ? (
              <Alert
                message="加载失败"
                description="无法加载项目数据，请检查网络连接"
                type="error"
                showIcon
              />
            ) : (
              <List
                itemLayout="horizontal"
                dataSource={projects}
                renderItem={(project: any) => (
                  <List.Item
                    actions={[
                      <Button icon={<EyeOutlined />} type="link">
                        查看
                      </Button>,
                      <Button icon={<EditOutlined />} type="link">
                        编辑
                      </Button>,
                      <Button icon={<DownloadOutlined />} type="link">
                        导出
                      </Button>,
                      <Button
                        icon={<DeleteOutlined />}
                        type="link"
                        danger
                        loading={deleteMutation.isPending}
                        onClick={() =>
                          handleDeleteProject(project.id.toString())
                        }
                      >
                        删除
                      </Button>,
                    ]}
                  >
                    <List.Item.Meta
                      title={
                        <Space>
                          {project.name}
                          <Tag color={getStatusColor(project.status)}>
                            {getStatusText(project.status)}
                          </Tag>
                          {project.file_size && (
                            <Text type="secondary" style={{ fontSize: "12px" }}>
                              {project.file_size.toFixed(2)}MB
                            </Text>
                          )}
                        </Space>
                      }
                      description={
                        <div>
                          <Text type="secondary">{project.description}</Text>
                          <br />
                          <Text type="secondary" style={{ fontSize: "12px" }}>
                            类型: {project.type} | 创建时间:{" "}
                            {new Date(project.created_at).toLocaleDateString()}
                            {project.assets_count > 0 &&
                              ` | 素材: ${project.assets_count}个`}
                          </Text>
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
            )}
          </Card>
        </Col>
      </Row>

      <Modal
        title="创建新项目"
        open={isModalVisible}
        onOk={handleCreateProject}
        onCancel={() => {
          setIsModalVisible(false);
          form.resetFields();
        }}
        okText="创建"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="项目名称"
            rules={[{ required: true, message: "请输入项目名称" }]}
          >
            <Input placeholder="输入项目名称" />
          </Form.Item>

          <Form.Item
            name="type"
            label="项目类型"
            rules={[{ required: true, message: "请选择项目类型" }]}
          >
            <Select placeholder="选择项目类型">
              <Option value="basic-project">基础项目</Option>
              <Option value="text-segment">文本片段</Option>
              <Option value="audio-segment">音频片段</Option>
              <Option value="video-segment">视频片段</Option>
              <Option value="comprehensive">综合项目</Option>
            </Select>
          </Form.Item>

          <Form.Item name="description" label="项目描述">
            <Input.TextArea rows={3} placeholder="输入项目描述（可选）" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ProjectManager;
