import React from 'react';
import { Row, Col, Card, Statistic, Progress, List, Badge, Space, Typography, Button, Spin, Alert } from 'antd';
import { useQuery } from '@tanstack/react-query';
import { 
  ApiOutlined, 
  ProjectOutlined, 
  CheckCircleOutlined, 
  ClockCircleOutlined,
  RocketOutlined,
  ThunderboltOutlined 
} from '@ant-design/icons';
import { Activity, Server, Zap, Film } from 'lucide-react';
import { apiService } from '@/services/api';

const { Title, Text, Paragraph } = Typography;

const Dashboard: React.FC = () => {
  const { data: healthData, isLoading, error } = useQuery({
    queryKey: ['health-check'],
    queryFn: apiService.healthCheck,
    refetchInterval: 30000,
  });

  const recentActivities = [
    { title: '创建基础项目', time: '2分钟前', status: 'success' },
    { title: '生成文本片段', time: '5分钟前', status: 'success' },
    { title: '添加视频动画', time: '10分钟前', status: 'processing' },
    { title: '导出项目文件', time: '15分钟前', status: 'success' },
  ];

  const quickActions = [
    { title: '创建基础项目', icon: <ProjectOutlined />, color: '#1890ff' },
    { title: '文本片段测试', icon: <ThunderboltOutlined />, color: '#52c41a' },
    { title: 'API 状态检查', icon: <ApiOutlined />, color: '#faad14' },
    { title: '综合功能测试', icon: <RocketOutlined />, color: '#f5222d' },
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
    <Spin spinning={isLoading}>
      <div>
        <div style={{ marginBottom: '24px' }}>
          <Title level={2}>
            <Space>
              <Film size={32} color="#1890ff" />
              仪表盘
            </Space>
          </Title>
          <Paragraph type="secondary">
            欢迎使用 pyJianYingDraft API Dashboard，这里是您的剪映草稿自动化控制中心
          </Paragraph>
        </div>

        <Row gutter={[16, 16]}>
          {/* 系统状态卡片 */}
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="API 状态"
                value={healthData?.status === 'running' ? '运行中' : '离线'}
                prefix={<Server size={16} />}
                valueStyle={{ color: healthData?.status === 'running' ? '#3f8600' : '#cf1322' }}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="可用接口"
                value={Object.keys(healthData?.endpoints || {}).length}
                prefix={<ApiOutlined />}
                suffix="个"
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="系统版本"
                value={healthData?.version || '1.0.0'}
                prefix={<Activity size={16} />}
                valueStyle={{ color: '#722ed1' }}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <div>
                <Text strong>系统性能</Text>
                <Progress 
                  percent={85} 
                  size="small" 
                  status="active"
                  style={{ marginTop: 8 }}
                />
                <Text type="secondary" style={{ fontSize: '12px' }}>
                  内存使用: 85%
                </Text>
              </div>
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
          {/* 快速操作 */}
          <Col xs={24} lg={12}>
            <Card title="🚀 快速操作" extra={<Button type="link">查看更多</Button>}>
              <Row gutter={[8, 8]}>
                {quickActions.map((action, index) => (
                  <Col span={12} key={index}>
                    <Card 
                      size="small" 
                      hoverable
                      style={{ textAlign: 'center', borderColor: action.color }}
                    >
                      <Space direction="vertical" size={4}>
                        <div style={{ color: action.color, fontSize: '24px' }}>
                          {action.icon}
                        </div>
                        <Text strong style={{ fontSize: '12px' }}>
                          {action.title}
                        </Text>
                      </Space>
                    </Card>
                  </Col>
                ))}
              </Row>
            </Card>
          </Col>
          
          {/* 最近活动 */}
          <Col xs={24} lg={12}>
            <Card title="📊 最近活动" extra={<Button type="link">查看全部</Button>}>
              <List
                size="small"
                dataSource={recentActivities}
                renderItem={(item) => (
                  <List.Item>
                    <Space>
                      <Badge 
                        status={item.status as any}
                        icon={item.status === 'success' ? <CheckCircleOutlined /> : <ClockCircleOutlined />}
                      />
                      <div>
                        <Text strong>{item.title}</Text>
                        <br />
                        <Text type="secondary" style={{ fontSize: '12px' }}>
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

        {/* API 接口列表 */}
        <Row style={{ marginTop: '24px' }}>
          <Col span={24}>
            <Card title="🔗 可用 API 接口">
              <Row gutter={[16, 16]}>
                {Object.entries(healthData?.endpoints || {}).map(([endpoint, description]) => (
                  <Col xs={24} sm={12} lg={8} key={endpoint}>
                    <Card size="small" hoverable>
                      <Space direction="vertical" size={4} style={{ width: '100%' }}>
                        <Text code style={{ fontSize: '12px' }}>
                          {endpoint}
                        </Text>
                        <Text type="secondary" style={{ fontSize: '12px' }}>
                          {description}
                        </Text>
                        <Button type="link" size="small" style={{ padding: 0 }}>
                          测试接口 →
                        </Button>
                      </Space>
                    </Card>
                  </Col>
                ))}
              </Row>
            </Card>
          </Col>
        </Row>
      </div>
    </Spin>
  );
};

export default Dashboard;
