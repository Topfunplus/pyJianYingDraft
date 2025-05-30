import React, { useState } from 'react';
import { 
  Card, Form, Input, Button, Select, Space, Typography, Row, Col, 
  Checkbox, InputNumber, ColorPicker, Tabs, Alert, Spin, Modal, message, List
} from 'antd';
import { useMutation } from '@tanstack/react-query';
import { 
  PlusOutlined, PlayCircleOutlined, FileTextOutlined, 
  AudioOutlined, VideoCameraOutlined, FontSizeOutlined,
  ThunderboltOutlined, BgColorsOutlined 
} from '@ant-design/icons';
import { Film, Sparkles } from 'lucide-react';
import Editor from '@monaco-editor/react';
import { apiService } from '@/services/api';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { TextArea } = Input;

interface ProjectSection {
  enabled: boolean;
  config: any;
}

interface ProjectData {
  text: ProjectSection;
  audio: ProjectSection;
  video: ProjectSection;
  animation: ProjectSection;
  effects: ProjectSection;
  transition: ProjectSection;
}

const CreateProject: React.FC = () => {
  const [form] = Form.useForm();
  const [projectData, setProjectData] = useState<ProjectData>({
    text: { enabled: true, config: {} },
    audio: { enabled: false, config: {} },
    video: { enabled: false, config: {} },
    animation: { enabled: false, config: {} },
    effects: { enabled: false, config: {} },
    transition: { enabled: false, config: {} },
  });
  const [previewVisible, setPreviewVisible] = useState(false);
  const [generatedResult, setGeneratedResult] = useState<any>(null);

  // 综合项目生成mutation
  const generateMutation = useMutation({
    mutationFn: async (config: any) => {
      console.log('开始调用API，配置:', config);
      try {
        // 调用新的综合创作API
        const result = await apiService.createComprehensiveProject(config);
        console.log('API调用成功:', result);
        return result;
      } catch (error) {
        console.error('API调用失败:', error);
        throw error;
      }
    },
    onSuccess: (data) => {
      console.log('项目生成成功:', data);
      setGeneratedResult(data);
      setPreviewVisible(true);
      message.success('项目生成成功！');
    },
    onError: (error: any) => {
      console.error('项目生成失败:', error);
      // 显示更详细的错误信息
      const errorMessage = error?.response?.data?.message || error?.message || '未知错误';
      message.error(`项目生成失败: ${errorMessage}`);
    },
  });

  const handleSectionToggle = (section: keyof ProjectData, enabled: boolean) => {
    setProjectData(prev => ({
      ...prev,
      [section]: { ...prev[section], enabled }
    }));
  };

  const handleConfigChange = (section: keyof ProjectData, config: any) => {
    setProjectData(prev => ({
      ...prev,
      [section]: { ...prev[section], config }
    }));
  };

  const handleGenerate = () => {
    try {
      console.log('开始生成项目...');
      const formData = form.getFieldsValue();
      console.log('表单数据:', formData);
      console.log('项目状态:', projectData);
      
      // 构建配置对象
      const config: any = {};
      Object.keys(projectData).forEach(key => {
        const section = projectData[key as keyof ProjectData];
        config[key] = {
          enabled: section.enabled,
          config: { 
            ...section.config, 
            ...(formData[key] || {})
          }
        };
      });

      console.log('最终配置:', config);
      
      // 检查是否有启用的组件
      const hasEnabledComponents = Object.values(config).some((item: any) => item.enabled);
      if (!hasEnabledComponents) {
        message.warning('请至少启用一个组件');
        return;
      }

      generateMutation.mutate(config);
    } catch (error) {
      console.error('配置生成失败:', error);
      message.error('配置生成失败，请检查输入参数');
    }
  };

  const sectionConfigs = [
    {
      key: 'text',
      title: '文本片段',
      icon: <FontSizeOutlined />,
      color: '#1890ff',
      description: '添加文字内容和样式',
      fields: [
        { name: 'text', label: '文本内容', type: 'textarea', default: '欢迎使用剪映助手' },
        { name: 'duration', label: '显示时长', type: 'input', default: '3s' },
        { name: 'font', label: '字体', type: 'select', options: ['文轩体', '思源黑体', '微软雅黑'] },
        { name: 'color', label: '文字颜色', type: 'color', default: [1.0, 1.0, 1.0] },
      ]
    },
    {
      key: 'audio',
      title: '音频片段',
      icon: <AudioOutlined />,
      color: '#52c41a',
      description: '配置音频参数',
      fields: [
        { name: 'duration', label: '音频时长', type: 'input', default: '5s' },
        { name: 'volume', label: '音量大小', type: 'number', default: 0.6, min: 0, max: 1, step: 0.1 },
        { name: 'fade_in', label: '淡入时间', type: 'input', default: '1s' },
      ]
    },
    {
      key: 'video',
      title: '视频片段',
      icon: <VideoCameraOutlined />,
      color: '#fa8c16',
      description: '设置视频参数',
      fields: [
        { name: 'duration', label: '视频时长', type: 'input', default: '4.2s' },
      ]
    },
    {
      key: 'animation',
      title: '动画效果',
      icon: <ThunderboltOutlined />,
      color: '#eb2f96',
      description: '添加动画特效',
      fields: [
        { name: 'text', label: '动画文本', type: 'input', default: '动画效果展示' },
        { name: 'animation_type', label: '动画类型', type: 'select', options: ['渐显', '淡入', '弹跳', '故障闪动'] },
        { name: 'duration', label: '持续时间', type: 'input', default: '2s' },
      ]
    },
    {
      key: 'effects',
      title: '文本特效',
      icon: <BgColorsOutlined />,
      color: '#722ed1',
      description: '气泡和花字效果',
      fields: [
        { name: 'text', label: '特效文本', type: 'input', default: '特效文字' },
        { name: 'effect_type', label: '特效类型', type: 'select', options: ['bubble', 'flower'] },
        { name: 'duration', label: '显示时长', type: 'input', default: '3s' },
      ]
    },
    {
      key: 'transition',
      title: '转场效果',
      icon: <PlayCircleOutlined />,
      color: '#13c2c2',
      description: '视频转场过渡',
      fields: [
        { name: 'transition_type', label: '转场类型', type: 'select', options: ['信号故障', '淡化', '滑动'] },
        { name: 'segment1_duration', label: '前段时长', type: 'input', default: '2s' },
        { name: 'segment2_duration', label: '后段时长', type: 'input', default: '2s' },
      ]
    },
  ];

  const tabItems = sectionConfigs.map(section => ({
    key: section.key,
    label: (
      <Space>
        <span style={{ color: section.color }}>{section.icon}</span>
        {section.title}
      </Space>
    ),
    children: (
      <div>
        <div style={{ marginBottom: 16 }}>
          <Checkbox
            checked={projectData[section.key as keyof ProjectData].enabled}
            onChange={(e) => handleSectionToggle(section.key as keyof ProjectData, e.target.checked)}
          >
            <Text strong>启用 {section.title}</Text>
          </Checkbox>
          <br />
          <Text type="secondary">{section.description}</Text>
        </div>

        {projectData[section.key as keyof ProjectData].enabled && (
          <Row gutter={[16, 16]}>
            {section.fields.map(field => (
              <Col xs={24} sm={12} lg={8} key={field.name}>
                <Form.Item
                  name={[section.key, field.name]}
                  label={field.label}
                  initialValue={field.default}
                >
                  {field.type === 'textarea' ? (
                    <TextArea rows={3} />
                  ) : field.type === 'select' ? (
                    <Select>
                      {field.options?.map(option => (
                        <Option key={option} value={option}>{option}</Option>
                      ))}
                    </Select>
                  ) : field.type === 'number' ? (
                    <InputNumber 
                      min={field.min} 
                      max={field.max} 
                      step={field.step}
                      style={{ width: '100%' }}
                    />
                  ) : field.type === 'color' ? (
                    <ColorPicker />
                  ) : (
                    <Input />
                  )}
                </Form.Item>
              </Col>
            ))}
          </Row>
        )}
      </div>
    ),
  }));

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <Title level={2}>
          <Space>
            <Film size={32} color="#1890ff" />
            开始创作
          </Space>
        </Title>
        <Paragraph type="secondary">
          配置多媒体组件，一键生成综合剪映项目。支持文本、音频、视频、动画、特效等多种元素组合。
        </Paragraph>
      </div>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={16}>
          <Card 
            title={
              <Space>
                <Sparkles size={20} color="#1890ff" />
                项目配置
              </Space>
            }
          >
            <Form form={form} layout="vertical">
              <Tabs
                defaultActiveKey="text"
                items={tabItems}
                tabPosition="top"
                size="small"
              />
            </Form>
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card title="🎬 项目概览">
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <Text strong>已启用组件:</Text>
                <div style={{ marginTop: 8 }}>
                  {Object.entries(projectData).map(([key, section]) => (
                    <div key={key} style={{ marginBottom: 4 }}>
                      <Checkbox 
                        checked={section.enabled} 
                        disabled
                        style={{ pointerEvents: 'none' }}
                      />
                      <Text style={{ marginLeft: 8, color: section.enabled ? '#1890ff' : '#999' }}>
                        {sectionConfigs.find(s => s.key === key)?.title}
                      </Text>
                    </div>
                  ))}
                </div>
              </div>

              <Alert
                message="集成说明"
                description="所有选中的组件将被集成到一个统一的剪映项目JSON文件中，按时间轴顺序排列。"
                type="info"
                showIcon
              />

              <Button
                type="primary"
                size="large"
                icon={<PlusOutlined />}
                loading={generateMutation.isPending}
                onClick={handleGenerate}
                block
                style={{ marginTop: 16 }}
                disabled={generateMutation.isPending}
              >
                {generateMutation.isPending ? '生成中...' : '生成集成项目'}
              </Button>

              <Alert
                message="提示"
                description="至少选择一个组件才能生成项目。未选择组件时将生成默认综合项目。"
                type="info"
                showIcon
                style={{ marginTop: 16 }}
              />
            </Space>
          </Card>

          <Card title="🚀 快速模板" style={{ marginTop: 16 }}>
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button 
                size="small" 
                block 
                onClick={() => {
                  // 设置文本+动画模板
                  setProjectData(prev => ({
                    ...prev,
                    text: { enabled: true, config: {} },
                    animation: { enabled: true, config: {} }
                  }));
                  message.info('已应用文本动画模板');
                }}
              >
                📝 文本动画模板
              </Button>
              <Button 
                size="small" 
                block
                onClick={() => {
                  // 设置全功能模板
                  setProjectData(prev => {
                    const newData = { ...prev };
                    Object.keys(newData).forEach(key => {
                      newData[key as keyof ProjectData].enabled = true;
                    });
                    return newData;
                  });
                  message.info('已应用全功能模板');
                }}
              >
                🎊 全功能模板
              </Button>
              <Button 
                size="small" 
                block
                onClick={() => {
                  // 重置所有配置
                  setProjectData({
                    text: { enabled: true, config: {} },
                    audio: { enabled: false, config: {} },
                    video: { enabled: false, config: {} },
                    animation: { enabled: false, config: {} },
                    effects: { enabled: false, config: {} },
                    transition: { enabled: false, config: {} },
                  });
                  form.resetFields();
                  message.info('已重置所有配置');
                }}
              >
                🔄 重置配置
              </Button>
            </Space>
          </Card>
        </Col>
      </Row>

      {/* 结果预览模态框 */}
      <Modal
        title="🎉 项目生成完成"
        open={previewVisible}
        onCancel={() => {
          setPreviewVisible(false);
          setGeneratedResult(null);
        }}
        footer={[
          <Button key="close" onClick={() => {
            setPreviewVisible(false);
            setGeneratedResult(null);
          }}>
            关闭
          </Button>,
          <Button 
            key="copy" 
            type="primary" 
            onClick={() => {
              if (generatedResult) {
                navigator.clipboard.writeText(JSON.stringify(generatedResult, null, 2));
                message.success('已复制到剪贴板');
              }
            }}
          >
            复制结果
          </Button>,
          <Button
            key="download"
            onClick={() => {
              if (generatedResult) {
                const blob = new Blob([JSON.stringify(generatedResult, null, 2)], {
                  type: 'application/json'
                });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `project_${Date.now()}.json`;
                a.click();
                URL.revokeObjectURL(url);
                message.success('文件下载完成');
              }
            }}
          >
            下载文件
          </Button>,
        ]}
        width={900}
        destroyOnClose
      >
        {generatedResult ? (
          <div>
            <Alert
              message={generatedResult.message || '项目生成成功'}
              description={
                <div>
                  <div>项目总时长: {generatedResult.summary?.total_duration || '未知'}</div>
                  <div>包含组件: {generatedResult.summary?.components_count || 0} 个</div>
                  <div>启用功能: {generatedResult.summary?.enabled_features?.join(', ') || '无'}</div>
                </div>
              }
              type="success"
              showIcon
              style={{ marginBottom: 16 }}
            />
            
            <Tabs
              items={[
                {
                  key: 'json',
                  label: '完整JSON',
                  children: (
                    <div style={{ height: '400px' }}>
                      <Editor
                        height="100%"
                        defaultLanguage="json"
                        value={JSON.stringify(generatedResult.data || generatedResult, null, 2)}
                        options={{
                          readOnly: true,
                          minimap: { enabled: false },
                          fontSize: 12,
                          theme: 'vs-light',
                          wordWrap: 'on',
                        }}
                      />
                    </div>
                  )
                },
                {
                  key: 'summary',
                  label: '组件摘要',
                  children: (
                    <div style={{ height: '400px', overflow: 'auto' }}>
                      {generatedResult.summary?.segments?.length > 0 ? (
                        <List
                          size="small"
                          dataSource={generatedResult.summary.segments}
                          renderItem={(item: any) => (
                            <List.Item>
                              <List.Item.Meta
                                title={`${item.type} - ${item.start_time || '时间未知'}`}
                                description={
                                  <div>
                                    {item.content && <div>内容: {item.content}</div>}
                                    {item.duration && <div>时长: {item.duration}</div>}
                                    {item.note && <div style={{ color: '#faad14' }}>注意: {item.note}</div>}
                                  </div>
                                }
                              />
                            </List.Item>
                          )}
                        />
                      ) : (
                        <div style={{ textAlign: 'center', padding: '20px' }}>
                          <Text type="secondary">暂无组件信息</Text>
                        </div>
                      )}
                    </div>
                  )
                }
              ]}
            />
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin size="large" />
            <div style={{ marginTop: 16 }}>
              <Text>正在处理结果...</Text>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default CreateProject;
