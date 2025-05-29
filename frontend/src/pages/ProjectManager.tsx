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
} from "antd";
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  DownloadOutlined,
  EyeOutlined,
} from "@ant-design/icons";
import { ProjectOutlined } from "@ant-design/icons";

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
  const [projects, setProjects] = useState<Project[]>([
    {
      id: "1",
      name: "测试项目 1",
      type: "text-segment",
      status: "completed",
      createdAt: "2024-01-01",
      description: "基础文本片段测试项目",
    },
    {
      id: "2",
      name: "综合测试项目",
      type: "comprehensive",
      status: "draft",
      createdAt: "2024-01-02",
      description: "包含音视频和文本的综合项目",
    },
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

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
        setProjects(projects.filter((p) => p.id !== id));
        message.success("项目删除成功");
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

  return (
    <div>
      <div
        style={{
          marginBottom: "24px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}>
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
          onClick={() => setIsModalVisible(true)}>
          创建新项目
        </Button>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card>
            <List
              itemLayout="horizontal"
              dataSource={projects}
              renderItem={(project) => (
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
                      onClick={() => handleDeleteProject(project.id)}>
                      删除
                    </Button>,
                  ]}>
                  <List.Item.Meta
                    title={
                      <Space>
                        {project.name}
                        <Tag color={getStatusColor(project.status)}>
                          {getStatusText(project.status)}
                        </Tag>
                      </Space>
                    }
                    description={
                      <div>
                        <Text type="secondary">{project.description}</Text>
                        <br />
                        <Text type="secondary" style={{ fontSize: "12px" }}>
                          类型: {project.type} | 创建时间: {project.createdAt}
                        </Text>
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
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
        cancelText="取消">
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="项目名称"
            rules={[{ required: true, message: "请输入项目名称" }]}>
            <Input placeholder="输入项目名称" />
          </Form.Item>

          <Form.Item
            name="type"
            label="项目类型"
            rules={[{ required: true, message: "请选择项目类型" }]}>
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
