import React, { useState } from "react";
import {
  Row,
  Col,
  Card,
  Statistic,
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
  DesktopOutlined,
} from "@ant-design/icons";
import { Activity, Film } from "lucide-react";
import { apiService } from "../services/api";
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
            text: "桌面版测试文本",
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
      
      // 桌面版通知
      if (window.electronAPI) {
        window.electronAPI.showNotification(
          '剪映助手',
          `${getApiTitle(apiType)}执行成功！`
        );
      }
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
    { title: "启动桌面应用", time: "刚刚", status: "success" },
    { title: "创建基础项目", time: "2分钟前", status: "success" },
    { title: "生成文本片段", time: "5分钟前", status: "success" },
    { title: "下载补丁包", time: "10分钟前", status: "processing" },
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
        action={
          <Button 
            size="small" 
            danger 
            onClick={() => window.location.reload()}
          >
            重试连接
          </Button>
        }
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
              桌面版仪表盘
            </Space>
          </Title>
          <Paragraph type="secondary">
            <Space>
              <DesktopOutlined />
              欢迎使用剪映助手桌面版，享受更流畅的本地化体验
            </Space>
          </Paragraph>
        </div>

        {/* 统计概览 */}
        <Row gutter={[16, 16]} style={{ marginBottom: "24px" }}>
          <Col xs={24} sm={6}>
            <Card>
              <Statistic
                title="运行状态"
                value={healthData?.status === 'running' ? '正常' : '异常'}
                valueStyle={{ color: healthData?.status === 'running' ? '#3f8600' : '#cf1322' }}
                prefix={<CheckCircleOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={6}>
            <Card>
              <Statistic
                title="API版本"
                value={healthData?.version || '1.0.0'}
                prefix={<RocketOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={6}>
            <Card>
              <Statistic
                title="平台"
                value={window.electronAPI?.getPlatform() === 'win32' ? 'Windows' : 'Other'}
                prefix={<DesktopOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={6}>
            <Card>
              <Statistic
                title="今日操作"
                value={4}
                prefix={<Activity size={16} />}
              />
            </Card>
          </Col>
        </Row>

        {/* 快速操作和最近活动 */}
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            <Card
              title="🚀 快速操作"
              extra={
                <Button type="link" onClick={() => navigate("/create")}>
                  开始创作
                </Button>
              }
              style={{ height: "100%" }}>
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
                        minHeight: "80px",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
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
              <Alert
                message="桌面版优势"
                description="本地文件访问 | 系统通知 | 离线使用"
                type="info"
                showIcon
                style={{ marginTop: 16 }}
              />
            </Card>
          </Col>

          <Col xs={24} lg={12}>
            <Card title="📊 最近活动" style={{ height: "100%" }}>
              <List
                size="small"
                dataSource={recentActivities}
                renderItem={(item) => (
                  <List.Item>
                    <Space>
                      <Badge
                        status={item.status as "success" | "processing" | "default" | "error" | "warning"}
                      />
                      <div>
                        <Text strong>{item.title}</Text>
                        <br />
                        <Text type="secondary" style={{ fontSize: "12px" }}>
                          {item.time}
                        </Text>
                      </div>
                      <div style={{ marginLeft: 8 }}>
                        {item.status === "success" ? (
                          <CheckCircleOutlined style={{ color: '#52c41a' }} />
                        ) : (
                          <ClockCircleOutlined style={{ color: '#faad14' }} />
                        )}
                      </div>
                    </Space>
                  </List.Item>
                )}
              />
            </Card>
          </Col>
        </Row>

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
            <Button
              key="save"
              onClick={async () => {
                if (window.electronAPI && modalContent) {
                  const result = await window.electronAPI.saveFile(
                    `result_${Date.now()}.json`,
                    JSON.stringify(modalContent, null, 2)
                  );
                  if (result.success) {
                    message.success(`文件已保存到: ${result.path}`);
                  } else {
                    message.error(`保存失败: ${result.error}`);
                  }
                }
              }}>
              保存文件
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
