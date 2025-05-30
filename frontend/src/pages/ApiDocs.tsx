import React, { useState } from 'react';
import { 
  Card, Typography, Button, Space, Alert, Spin, Tabs, 
  Form, Input, Select, InputNumber, Switch, Row, Col,
  Modal, message, Collapse
} from 'antd';
import { 
  PlayCircleOutlined, ApiOutlined, CodeOutlined,
  SendOutlined, BugOutlined, FileTextOutlined
} from '@ant-design/icons';
import { Film } from 'lucide-react';
import Editor from '@monaco-editor/react';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { TextArea } = Input;
const { Panel } = Collapse;

interface ApiEndpoint {
  path: string;
  method: 'GET' | 'POST';
  title: string;
  description: string;
  parameters?: Array<{
    name: string;
    type: 'string' | 'number' | 'boolean' | 'object' | 'array';
    required?: boolean;
    default?: any;
    description?: string;
    options?: string[];
  }>;
  example?: any;
}

const ApiDocs: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [testResult, setTestResult] = useState<any>(null);
  const [selectedEndpoint, setSelectedEndpoint] = useState<string>('/api/health');
  const [customJson, setCustomJson] = useState<string>('');
  const [useCustomJson, setUseCustomJson] = useState(false);

  // API端点配置
  const apiEndpoints: Record<string, ApiEndpoint> = {
    '/api/health': {
      path: '/api/health',
      method: 'GET',
      title: '健康检查',
      description: '检查API服务状态和可用接口列表',
      parameters: []
    },
    '/api/basic-project': {
      path: '/api/basic-project',
      method: 'POST',
      title: '创建基础项目',
      description: '创建一个基础的剪映项目结构',
      parameters: []
    },
    '/api/text-segment': {
      path: '/api/text-segment',
      method: 'POST',
      title: '创建文本片段',
      description: '创建包含文本内容和样式的片段',
      parameters: [
        { name: 'text', type: 'string', default: '测试文本', description: '文本内容' },
        { name: 'duration', type: 'string', default: '3s', description: '显示时长' },
        { name: 'font', type: 'string', options: ['文轩体', '思源黑体', '微软雅黑'], description: '字体类型' },
        { name: 'color', type: 'array', default: [1.0, 1.0, 1.0], description: '文字颜色 [R, G, B]' }
      ],
      example: {
        text: '这是一个测试文本',
        duration: '3s',
        font: '文轩体',
        color: [1.0, 1.0, 0.0]
      }
    },
    '/api/audio-segment': {
      path: '/api/audio-segment',
      method: 'POST',
      title: '创建音频片段',
      description: '创建音频片段配置',
      parameters: [
        { name: 'duration', type: 'string', default: '5s', description: '音频时长' },
        { name: 'volume', type: 'number', default: 0.6, description: '音量大小 (0-1)' },
        { name: 'fade_in', type: 'string', default: '1s', description: '淡入时间' }
      ],
      example: {
        duration: '5s',
        volume: 0.6,
        fade_in: '1s'
      }
    },
    '/api/video-segment': {
      path: '/api/video-segment',
      method: 'POST',
      title: '创建视频片段',
      description: '创建视频片段配置',
      parameters: [
        { name: 'duration', type: 'string', default: '4.2s', description: '视频时长' }
      ],
      example: {
        duration: '4.2s'
      }
    },
    '/api/comprehensive-create': {
      path: '/api/comprehensive-create',
      method: 'POST',
      title: '综合创作项目',
      description: '创建包含多个组件的综合项目',
      parameters: [
        { name: 'text.enabled', type: 'boolean', default: true, description: '启用文本组件' },
        { name: 'text.config.text', type: 'string', default: '综合创作文本', description: '文本内容' },
        { name: 'text.config.duration', type: 'string', default: '3s', description: '文本显示时长' },
        { name: 'audio.enabled', type: 'boolean', default: true, description: '启用音频组件' },
        { name: 'audio.config.duration', type: 'string', default: '5s', description: '音频时长' },
        { name: 'audio.config.volume', type: 'number', default: 0.6, description: '音量大小' },
        { name: 'video.enabled', type: 'boolean', default: true, description: '启用视频组件' },
        { name: 'video.config.duration', type: 'string', default: '4.2s', description: '视频时长' },
        { name: 'animation.enabled', type: 'boolean', default: false, description: '启用动画组件' },
        { name: 'effects.enabled', type: 'boolean', default: false, description: '启用特效组件' },
        { name: 'transition.enabled', type: 'boolean', default: false, description: '启用转场组件' }
      ],
      example: {
        text: { 
          enabled: true, 
          config: { 
            text: 'API调试测试', 
            duration: '3s',
            color: [1.0, 1.0, 0.0],
            font: '文轩体'
          } 
        },
        audio: { 
          enabled: true, 
          config: { 
            duration: '5s', 
            volume: 0.6,
            fade_in: '1s'
          } 
        },
        video: { 
          enabled: true, 
          config: { 
            duration: '4.2s' 
          } 
        },
        animation: { 
          enabled: true, 
          config: { 
            text: '动画文本', 
            animation_type: '故障闪动',
            duration: '2s'
          } 
        }
      }
    },
    '/api/download-from-url': {
      path: '/api/download-from-url',
      method: 'POST',
      title: '网络下载文件',
      description: '从网址下载音视频文件到服务器',
      parameters: [
        { name: 'url', type: 'string', default: 'https://www.w3schools.com/html/mov_bbb.mp4', description: '文件网址' },
        { name: 'type', type: 'string', options: ['audio', 'video'], default: 'video', description: '文件类型' }
      ],
      example: {
        url: 'https://www.w3schools.com/html/mov_bbb.mp4',
        type: 'video'
      }
    }
  };

  const handleEndpointChange = (endpoint: string) => {
    setSelectedEndpoint(endpoint);
    setTestResult(null);
    setUseCustomJson(false);
    
    // 自动填充表单默认值
    const endpointConfig = apiEndpoints[endpoint];
    if (endpointConfig?.example) {
      setCustomJson(JSON.stringify(endpointConfig.example, null, 2));
    } else {
      setCustomJson('{}');
    }
    
    // 重置表单
    form.resetFields();
    
    // 填充默认值
    if (endpointConfig?.parameters) {
      const defaultValues: any = {};
      endpointConfig.parameters.forEach(param => {
        if (param.default !== undefined) {
          const keys = param.name.split('.');
          let current = defaultValues;
          for (let i = 0; i < keys.length - 1; i++) {
            if (!current[keys[i]]) current[keys[i]] = {};
            current = current[keys[i]];
          }
          current[keys[keys.length - 1]] = param.default;
        }
      });
      form.setFieldsValue(defaultValues);
    }
  };

  const buildRequestData = () => {
    if (useCustomJson) {
      try {
        return JSON.parse(customJson);
      } catch (e) {
        message.error('JSON格式错误，请检查语法');
        return null;
      }
    }

    const formData = form.getFieldsValue();
    const endpointConfig = apiEndpoints[selectedEndpoint];
    
    if (!endpointConfig?.parameters || endpointConfig.parameters.length === 0) {
      return null; // GET请求或无参数POST请求
    }

    // 构建嵌套对象
    const result: any = {};
    endpointConfig.parameters.forEach(param => {
      const keys = param.name.split('.');
      let current = result;
      let formValue = formData;
      
      // 获取表单值
      for (const key of keys) {
        if (formValue && typeof formValue === 'object') {
          formValue = formValue[key];
        } else {
          formValue = undefined;
          break;
        }
      }
      
      // 设置值到结果对象
      for (let i = 0; i < keys.length - 1; i++) {
        if (!current[keys[i]]) current[keys[i]] = {};
        current = current[keys[i]];
      }
      
      if (formValue !== undefined) {
        current[keys[keys.length - 1]] = formValue;
      } else if (param.default !== undefined) {
        current[keys[keys.length - 1]] = param.default;
      }
    });

    return result;
  };

  const testApi = async () => {
    setLoading(true);
    setTestResult(null);

    try {
      const endpointConfig = apiEndpoints[selectedEndpoint];
      const requestData = buildRequestData();

      console.log('🚀 测试API:', selectedEndpoint);
      console.log('📝 请求数据:', requestData);

      const options: RequestInit = {
        method: endpointConfig.method,
        headers: { 'Content-Type': 'application/json' }
      };

      if (requestData && endpointConfig.method === 'POST') {
        options.body = JSON.stringify(requestData);
      }

      const startTime = Date.now();
      const response = await fetch(selectedEndpoint, options);
      const endTime = Date.now();
      
      let responseData;
      const contentType = response.headers.get('content-type');
      
      if (contentType && contentType.includes('application/json')) {
        responseData = await response.json();
      } else {
        responseData = await response.text();
      }

      setTestResult({
        success: response.ok,
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries(response.headers.entries()),
        data: responseData,
        responseTime: endTime - startTime,
        requestData: requestData,
        endpoint: selectedEndpoint,
        method: endpointConfig.method
      });

      if (response.ok) {
        message.success(`API调用成功 (${endTime - startTime}ms)`);
      } else {
        message.error(`API调用失败: ${response.status}`);
      }

    } catch (error: any) {
      console.error('API测试失败:', error);
      setTestResult({
        success: false,
        error: error.message,
        endpoint: selectedEndpoint,
        requestData: buildRequestData()
      });
      message.error(`网络错误: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const renderParameterForm = () => {
    const endpointConfig = apiEndpoints[selectedEndpoint];
    
    if (!endpointConfig?.parameters || endpointConfig.parameters.length === 0) {
      return (
        <Alert 
          message="此接口无需参数" 
          type="info" 
          style={{ marginBottom: 16 }}
        />
      );
    }

    return (
      <Form form={form} layout="vertical">
        <Row gutter={[16, 16]}>
          {endpointConfig.parameters.map((param) => (
            <Col xs={24} sm={12} lg={8} key={param.name}>
              <Form.Item
                name={param.name.split('.')}
                label={
                  <Space>
                    <Text strong>{param.name}</Text>
                    {param.required && <Text type="danger">*</Text>}
                  </Space>
                }
                help={param.description}
                rules={param.required ? [{ required: true, message: `请输入${param.name}` }] : []}
              >
                {param.type === 'boolean' ? (
                  <Switch defaultChecked={param.default} />
                ) : param.type === 'number' ? (
                  <InputNumber style={{ width: '100%' }} placeholder={`默认: ${param.default}`} />
                ) : param.options ? (
                  <Select placeholder={`选择${param.name}`} allowClear>
                    {param.options.map(option => (
                      <Option key={option} value={option}>{option}</Option>
                    ))}
                  </Select>
                ) : param.type === 'array' ? (
                  <Input placeholder={`例如: ${JSON.stringify(param.default)}`} />
                ) : (
                  <Input placeholder={`默认: ${param.default}`} />
                )}
              </Form.Item>
            </Col>
          ))}
        </Row>
      </Form>
    );
  };

  const currentEndpoint = apiEndpoints[selectedEndpoint];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '24px' }}>
        <Title level={2}>
          <Space>
            <Film size={32} color="#1890ff" />
            API 测试调试
          </Space>
        </Title>
        <Paragraph type="secondary">
          交互式API接口测试工具，支持参数配置和实时调试
        </Paragraph>
      </div>

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={14}>
          <Card title={
            <Space>
              <BugOutlined />
              接口调试
            </Space>
          }>
            {/* 接口选择 */}
            <div style={{ marginBottom: 24 }}>
              <Text strong>选择API接口:</Text>
              <Select
                value={selectedEndpoint}
                onChange={handleEndpointChange}
                style={{ width: '100%', marginTop: 8 }}
                size="large"
              >
                {Object.entries(apiEndpoints).map(([path, config]) => (
                  <Option key={path} value={path}>
                    <Space>
                      <span style={{
                        padding: '2px 6px',
                        borderRadius: '4px',
                        fontSize: '12px',
                        backgroundColor: config.method === 'GET' ? '#52c41a' : '#1890ff',
                        color: 'white'
                      }}>
                        {config.method}
                      </span>
                      {config.title}
                    </Space>
                  </Option>
                ))}
              </Select>
            </div>

            {/* 接口信息 */}
            <Alert
              message={currentEndpoint?.title}
              description={currentEndpoint?.description}
              type="info"
              style={{ marginBottom: 24 }}
            />

            {/* 参数配置方式选择 */}
            {currentEndpoint?.method === 'POST' && (
              <div style={{ marginBottom: 24 }}>
                <Space>
                  <Text strong>参数配置方式:</Text>
                  <Button.Group>
                    <Button 
                      type={!useCustomJson ? 'primary' : 'default'}
                      onClick={() => setUseCustomJson(false)}
                    >
                      表单模式
                    </Button>
                    <Button 
                      type={useCustomJson ? 'primary' : 'default'}
                      onClick={() => setUseCustomJson(true)}
                    >
                      JSON模式
                    </Button>
                  </Button.Group>
                </Space>
              </div>
            )}

            {/* 参数配置区域 */}
            {currentEndpoint?.method === 'POST' && (
              <div style={{ marginBottom: 24 }}>
                {useCustomJson ? (
                  <div>
                    <Text strong>JSON参数:</Text>
                    <div style={{ marginTop: 8, border: '1px solid #d9d9d9', borderRadius: '6px' }}>
                      <Editor
                        height="300px"
                        defaultLanguage="json"
                        value={customJson}
                        onChange={(value) => setCustomJson(value || '{}')}
                        options={{
                          minimap: { enabled: false },
                          fontSize: 14,
                          wordWrap: 'on',
                          formatOnPaste: true,
                          formatOnType: true
                        }}
                      />
                    </div>
                  </div>
                ) : (
                  <div>
                    <Text strong>参数配置:</Text>
                    <div style={{ marginTop: 16 }}>
                      {renderParameterForm()}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* 测试按钮 */}
            <Button
              type="primary"
              size="large"
              icon={<SendOutlined />}
              loading={loading}
              onClick={testApi}
              block
            >
              {loading ? '测试中...' : '发送请求'}
            </Button>
          </Card>
        </Col>

        <Col xs={24} lg={10}>
          <Card title={
            <Space>
              <CodeOutlined />
              测试结果
            </Space>
          }>
            {testResult ? (
              <div>
                {/* 响应概要 */}
                <div style={{ marginBottom: 16 }}>
                  <Alert
                    message={
                      <Space>
                        <span>状态: {testResult.status}</span>
                        {testResult.responseTime && (
                          <span>响应时间: {testResult.responseTime}ms</span>
                        )}
                      </Space>
                    }
                    type={testResult.success ? 'success' : 'error'}
                  />
                </div>

                {/* 详细结果 */}
                <Collapse>
                  <Panel header="请求信息" key="request">
                    <div style={{ background: '#f6f8fa', padding: '12px', borderRadius: '4px' }}>
                      <Text strong>请求地址:</Text>
                      <div style={{ fontFamily: 'monospace', fontSize: '12px', marginBottom: '8px' }}>
                        {testResult.method} {testResult.endpoint}
                      </div>
                      
                      {testResult.requestData && (
                        <>
                          <Text strong>请求参数:</Text>
                          <pre style={{ fontSize: '12px', marginTop: '4px', overflow: 'auto' }}>
                            {JSON.stringify(testResult.requestData, null, 2)}
                          </pre>
                        </>
                      )}
                    </div>
                  </Panel>
                  
                  <Panel header="响应数据" key="response">
                    <div style={{ background: '#f6f8fa', padding: '12px', borderRadius: '4px' }}>
                      <pre style={{ fontSize: '12px', overflow: 'auto', maxHeight: '400px' }}>
                        {typeof testResult.data === 'string' 
                          ? testResult.data 
                          : JSON.stringify(testResult.data, null, 2)}
                      </pre>
                    </div>
                  </Panel>
                  
                  {testResult.headers && (
                    <Panel header="响应头" key="headers">
                      <div style={{ background: '#f6f8fa', padding: '12px', borderRadius: '4px' }}>
                        <pre style={{ fontSize: '12px' }}>
                          {JSON.stringify(testResult.headers, null, 2)}
                        </pre>
                      </div>
                    </Panel>
                  )}
                  
                  {testResult.error && (
                    <Panel header="错误信息" key="error">
                      <Alert
                        message="请求失败"
                        description={testResult.error}
                        type="error"
                      />
                    </Panel>
                  )}
                </Collapse>
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '40px 20px', color: '#999' }}>
                <ApiOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
                <div>选择接口并点击"发送请求"开始测试</div>
              </div>
            )}
          </Card>
        </Col>
      </Row>

      {/* API文档链接 */}
      <Card style={{ marginTop: 24 }}>
        <div style={{ textAlign: 'center' }}>
          <Space direction="vertical" size="middle">
            <FileTextOutlined style={{ fontSize: '32px', color: '#1890ff' }} />
            <Title level={4}>更多API信息</Title>
            <Space>
              <Button 
                type="primary" 
                href="/api/health" 
                target="_blank"
                icon={<ApiOutlined />}
              >
                查看完整API文档
              </Button>
              <Button 
                href="/"
                target="_blank"
              >
                在线文档页面
              </Button>
            </Space>
          </Space>
        </div>
      </Card>
    </div>
  );
};

export default ApiDocs;
