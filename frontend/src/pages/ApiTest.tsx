import React, { useState } from 'react';
import { Row, Col, Card, Form, Input, Button, Select, Space, Typography, Alert, Spin, Tabs } from 'antd';
import { useMutation } from '@tanstack/react-query';
import { PlayCircleOutlined, ApiOutlined, FileTextOutlined } from '@ant-design/icons';
import Editor from '@monaco-editor/react';
import { apiService, ProjectConfig } from '../services/api';

const { Title, Text } = Typography;
const { Option } = Select;
const { TextArea } = Input;

const ApiTest: React.FC = () => {
  const [form] = Form.useForm();
  const [responseData, setResponseData] = useState<any>(null);
  const [selectedApi, setSelectedApi] = useState<string>('basic-project');

  // API调用mutation
  const apiMutation = useMutation({
    mutationFn: async ({ apiType, config }: { apiType: string; config?: ProjectConfig }) => {
      switch (apiType) {
        case 'basic-project':
          return apiService.createBasicProject();
        case 'text-segment':
          return apiService.createTextSegment(config || {});
        case 'audio-segment':
          return apiService.createAudioSegment(config || {});
        case 'video-segment':
          return apiService.createVideoSegment(config || {});
        case 'video-animation':
          return apiService.createVideoAnimation(config || {});
        case 'text-animation':
          return apiService.createTextAnimation(config || {});
        case 'transition':
          return apiService.createTransition(config || {});
        case 'background-filling':
          return apiService.createBackgroundFilling(config || {});
        case 'text-effects':
          return apiService.createTextEffects(config || {});
        case 'comprehensive':
          return apiService.createComprehensive();
        default:
          throw new Error('未知的API类型');
      }
    },
    onSuccess: (data) => {
      setResponseData(data);
    },
  });

  const handleTest = () => {
    const config = form.getFieldsValue();
    apiMutation.mutate({ apiType: selectedApi, config });
  };

  const apiConfigs = {
    'basic-project': {
      title: '基础项目',
      fields: [],
    },
    'text-segment': {
      title: '文本片段',
      fields: [
        { name: 'text', label: '文本内容', type: 'input', default: '测试文本' },
        { name: 'duration', label: '持续时长', type: 'input', default: '3s' },
        { name: 'font', label: '字体', type: 'select', options: ['文轩体', '思源黑体', '微软雅黑'] },
      ],
    },
    'audio-segment': {
      title: '音频片段',
      fields: [
        { name: 'duration', label: '持续时长', type: 'input', default: '5s' },
        { name: 'volume', label: '音量', type: 'number', default: 0.6 },
        { name: 'fade_in', label: '淡入时间', type: 'input', default: '1s' },
      ],
    },
    'video-segment': {
      title: '视频片段',
      fields: [
        { name: 'duration', label: '持续时长', type: 'input', default: '4.2s' },
      ],
    },
    'text-animation': {
      title: '文本动画',
      fields: [
        { name: 'text', label: '文本内容', type: 'input', default: '动画文本' },
        { name: 'animation_type', label: '动画类型', type: 'select', options: ['渐显', '淡入', '弹跳'] },
        { name: 'duration', label: '持续时长', type: 'input', default: '2s' },
      ],
    },
  };

  const tabItems = [
    {
      key: 'form',
      label: '表单测试',
      children: (
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={12}>
            <Card title="API 配置" extra={<ApiOutlined />}>
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <Text strong>选择 API:</Text>
                  <Select
                    style={{ width: '100%', marginTop: 8 }}
                    value={selectedApi}
                    onChange={setSelectedApi}
                  >
                    {Object.entries(apiConfigs).map(([key, config]) => (
                      <Option key={key} value={key}>
                        {config.title}
                      </Option>
                    ))}
                  </Select>
                </div>

                <Form form={form} layout="vertical">
                  {apiConfigs[selectedApi as keyof typeof apiConfigs]?.fields.map((field) => (
                    <Form.Item
                      key={field.name}
                      name={field.name}
                      label={field.label}
                      initialValue={field.default}
                    >
                      {field.type === 'select' ? (
                        <Select>
                          {field.options?.map((option) => (
                            <Option key={option} value={option}>
                              {option}
                            </Option>
                          ))}
                        </Select>
                      ) : field.type === 'number' ? (
                        <Input type="number" step="0.1" />
                      ) : (
                        <Input />
                      )}
                    </Form.Item>
                  ))}
                </Form>

                <Button
                  type="primary"
                  icon={<PlayCircleOutlined />}
                  loading={apiMutation.isPending}
                  onClick={handleTest}
                  size="large"
                  block
                >
                  测试 API
                </Button>
              </Space>
            </Card>
          </Col>

          <Col xs={24} lg={12}>
            <Card title="响应结果" extra={<FileTextOutlined />}>
              <Spin spinning={apiMutation.isPending}>
                {apiMutation.error && (
                  <Alert
                    message="请求失败"
                    description={String(apiMutation.error)}
                    type="error"
                    showIcon
                    style={{ marginBottom: 16 }}
                  />
                )}
                
                {responseData && (
                  <div style={{ height: '400px' }}>
                    <Editor
                      height="100%"
                      defaultLanguage="json"
                      value={JSON.stringify(responseData, null, 2)}
                      options={{
                        readOnly: true,
                        minimap: { enabled: false },
                        fontSize: 12,
                      }}
                    />
                  </div>
                )}
              </Spin>
            </Card>
          </Col>
        </Row>
      ),
    },
    {
      key: 'raw',
      label: '原始请求',
      children: (
        <div>
          <Text type="secondary">直接发送JSON请求到API端点</Text>
          {/* 这里可以添加原始请求功能 */}
        </div>
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <Title level={2}>
          <Space>
            <ApiOutlined />
            API 测试工具
          </Space>
        </Title>
        <Text type="secondary">
          测试 pyJianYingDraft API 接口，查看响应结果
        </Text>
      </div>

      <Tabs defaultActiveKey="form" items={tabItems} />
    </div>
  );
};

export default ApiTest;
