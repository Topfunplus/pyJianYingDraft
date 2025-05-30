import React, { useState } from "react";
import {
  Row,
  Col,
  Card,
  Statistic,
  Progress,
  List,
  Badge,
  Space,
  Typography,
  Button,
  Spin,
  Alert,
  Modal,
  message,
} from "antd";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import {
  ProjectOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  RocketOutlined,
  ThunderboltOutlined,
} from "@ant-design/icons";
import { Activity, Server, Film } from "lucide-react";
import { apiService } from "@/services/api";
import Editor from "@monaco-editor/react";

const { Title, Text, Paragraph } = Typography;

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [modalVisible, setModalVisible] = useState(false);
  const [modalContent, setModalContent] = useState<any>(null);
  const [modalTitle, setModalTitle] = useState("");

  const {
    data: healthData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["health-check"],
    queryFn: apiService.healthCheck,
    refetchInterval: 30000,
  });

  // API测试mutation
  const testMutation = useMutation({
    mutationFn: async (apiType: string) => {
      switch (apiType) {
        case "basic-project":
          return apiService.createBasicProject();
        case "text-segment":
          return apiService.createTextSegment({
            text: "仪表盘测试文本",
            duration: "2s",
          });
        case "comprehensive":
          return apiService.createComprehensive();
        default:
          throw new Error("未知的API类型");
      }
    },
    onSuccess: (data, apiType) => {
      setModalTitle(`${getApiTitle(apiType)} - 测试结果`);
      setModalContent(data);
      setModalVisible(true);
      message.success(`${getApiTitle(apiType)}调用成功`);
    },
    onError: (error, apiType) => {
      message.error(`${getApiTitle(apiType)}调用失败: ${error}`);
    },
  });

  const getApiTitle = (apiType: string) => {
    const titles: { [key: string]: string } = {
      "basic-project": "创建基础项目",
      "text-segment": "文本片段测试",
      comprehensive: "综合功能测试",
    };
    return titles[apiType] || apiType;
  };

  const handleQuickAction = (actionType: string) => {
    testMutation.mutate(actionType);
  };

  const recentActivities = [
    { title: "创建基础项目", time: "2分钟前", status: "success" },
    { title: "生成文本片段", time: "5分钟前", status: "success" },
    { title: "添加视频动画", time: "10分钟前", status: "processing" },
    { title: "导出项目文件", time: "15分钟前", status: "success" },
  ];

  const quickActions = [
    {
      title: "创建基础项目",
      icon: <ProjectOutlined />,
      color: "#1890ff",
      action: "basic-project",
    },
    {
      title: "文本片段测试",
      icon: <ThunderboltOutlined />,
      color: "#52c41a",
      action: "text-segment",
    },
    {
      title: "综合功能测试",
      icon: <RocketOutlined />,
      color: "#f5222d",
      action: "comprehensive",
    },
  ];

  if (error) {
    return (
      <Alert
        message="连接失败"
        description="无法连接到后端API服务，请检查服务是否正常运行"
        type="error"
        showIcon
      />
    );
  }

  return (
    <Spin spinning={isLoading || testMutation.isPending}>
      <div>
        <div style={{ marginBottom: "24px" }}>
          <Title level={2}>
            <Space>
              <Film size={32} color="#1890ff" />
              仪表盘
            </Space>
          </Title>
          <Paragraph type="secondary">
            欢迎使用 pyJianYingDraft 控制中心，这里是您的剪映草稿自动化控制中心
          </Paragraph>
        </div>

        <Row gutter={[16, 16]}>
          {/* 系统状态卡片 - 删除API状态，保留其他卡片 */}
          <Col xs={24} sm={12} lg={8}>
            <Card>
              <Statistic
                title="系统版本"
                value={healthData?.version || "1.0.0"}
                prefix={<Activity size={16} />}
                valueStyle={{ color: "#722ed1" }}
              />
            </Card>
          </Col>

          <Col xs={24} sm={12} lg={8}>
            <Card>
              <div>
                <Text strong>系统性能</Text>
                <Progress
                  percent={85}
                  size="small"
                  status="active"
                  style={{ marginTop: 8 }}
                />
                <Text type="secondary" style={{ fontSize: "12px" }}>
                  内存使用: 85%
                </Text>
              </div>
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]} style={{ marginTop: "24px" }}>
          {/* 快速操作 */}
          <Col xs={24} lg={12}>
            <Card
              title="🚀 快速操作"
              extra={
                <Button type="link" onClick={() => navigate("/create")}>
                  开始创作
                </Button>
              }>
              <Row gutter={[8, 8]}>
                {quickActions.map((action, index) => (
                  <Col span={12} key={index}>
                    <Card
                      size="small"
                      hoverable
                      style={{
                        textAlign: "center",
                        borderColor: action.color,
                        cursor: "pointer",
                      }}
                      onClick={() => handleQuickAction(action.action)}>
                      <Space direction="vertical" size={4}>
                        <div style={{ color: action.color, fontSize: "24px" }}>
                          {action.icon}
                        </div>
                        <Text strong style={{ fontSize: "12px" }}>
                          {action.title}
                        </Text>
                      </Space>
                    </Card>
                  </Col>
                ))}
              </Row>
            </Card>
          </Col>

          {/* 最近活动 - 移除了查看全部按钮，它指向项目管理页面 */}
          <Col xs={24} lg={12}>
            <Card title="📊 最近活动">
              <List
                size="small"
                dataSource={recentActivities}
                renderItem={(item) => (
                  <List.Item>
                    <Space>
                      <Badge
                        status={item.status as any}
                        icon={
                          item.status === "success" ? (
                            <CheckCircleOutlined />
                          ) : (
                            <ClockCircleOutlined />
                          )
                        }
                      />
                      <div>
                        <Text strong>{item.title}</Text>
                        <br />
                        <Text type="secondary" style={{ fontSize: "12px" }}>
                          {item.time}
                        </Text>
                      </div>
                    </Space>
                  </List.Item>
                )}
              />
            </Card>
          </Col>
        </Row>

        {/* 删除API接口列表部分 */}

        {/* 结果显示模态框 */}
        <Modal
          title={modalTitle}
          open={modalVisible}
          onCancel={() => setModalVisible(false)}
          footer={[
            <Button key="close" onClick={() => setModalVisible(false)}>
              关闭
            </Button>,
            <Button
              key="copy"
              type="primary"
              onClick={() => {
                navigator.clipboard.writeText(
                  JSON.stringify(modalContent, null, 2)
                );
                message.success("已复制到剪贴板");
              }}>
              复制结果
            </Button>,
          ]}
          width={800}>
          {modalContent && (
            <div style={{ height: "400px" }}>
              <Editor
                height="100%"
                defaultLanguage="json"
                value={JSON.stringify(modalContent, null, 2)}
                options={{
                  readOnly: true,
                  minimap: { enabled: false },
                  fontSize: 12,
                  theme: "vs-light",
                }}
              />
            </div>
          )}
        </Modal>
      </div>
    </Spin>
  );
};

export default Dashboard;
