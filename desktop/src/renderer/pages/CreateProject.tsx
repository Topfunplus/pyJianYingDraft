import React, { useState } from 'react';
import { 
  Card, Form, Input, Button, Select, Space, Typography, Row, Col, 
  Checkbox, InputNumber, ColorPicker, Tabs, Alert, Spin, Modal, message, 
  List, Upload, Tag, Collapse
} from 'antd';
import { useMutation } from '@tanstack/react-query';
import { 
  PlusOutlined, PlayCircleOutlined, FileTextOutlined, 
  AudioOutlined, VideoCameraOutlined, FontSizeOutlined,
  ThunderboltOutlined, BgColorsOutlined, UploadOutlined, DeleteOutlined,
  DownloadOutlined, FolderOpenOutlined
} from '@ant-design/icons';
import { Film, Sparkles } from 'lucide-react';
import Editor from '@monaco-editor/react';
import { apiService } from '../services/api';
import PathSelectModal from '../components/PathSelectModal';

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

interface UploadedAsset {
  file?: File;
  filename: string;
  type: 'audio' | 'video';
  url?: string;
  source: 'upload' | 'download';
  size?: number;
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
  const [uploadedAssets, setUploadedAssets] = useState<UploadedAsset[]>([]);
  const [pathModalVisible, setPathModalVisible] = useState(false);
  const [currentProjectData, setCurrentProjectData] = useState<any>(null);
  const [downloadLoading, setDownloadLoading] = useState(false);
  const [createLoading, setCreateLoading] = useState(false);

  // 综合项目生成mutation
  const generateMutation = useMutation({
    mutationFn: async (config: any) => {
      console.log('开始调用API，配置:', config);
      try {
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
      
      // 桌面版通知
      if (window.electronAPI) {
        window.electronAPI.showNotification(
          '剪映助手',
          '项目生成完成！'
        );
      }
    },
    onError: (error: any) => {
      console.error('项目生成失败:', error);
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

  const handleGenerate = () => {
    try {
      console.log('开始生成项目...');
      const formData = form.getFieldsValue();
      console.log('表单数据:', formData);
      console.log('项目状态:', projectData);
      
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

  const handleFileUpload = (file: File, type: 'audio' | 'video') => {
    const url = URL.createObjectURL(file);
    const asset: UploadedAsset = {
      file,
      filename: file.name,
      type,
      url,
      source: 'upload',
      size: file.size
    };
    
    setUploadedAssets(prev => [
      ...prev.filter(item => item.type !== type),
      asset
    ]);
    
    message.success(`${type === 'audio' ? '音频' : '视频'}文件上传成功`);
    return false;
  };

  const removeAsset = (type: 'audio' | 'video') => {
    setUploadedAssets(prev => {
      const removed = prev.find(item => item.type === type);
      if (removed?.url) {
        URL.revokeObjectURL(removed.url);
      }
      return prev.filter(item => item.type !== type);
    });
    message.success(`${type === 'audio' ? '音频' : '视频'}文件已移除`);
  };

  const handleDownloadPatch = async () => {
    try {
      setCreateLoading(true);
      message.loading({ content: '正在准备项目数据...', key: 'create' });

      if (generatedResult?.data) {
        setCurrentProjectData(generatedResult.data);
        message.success({ content: '使用当前项目数据，请选择工程目录', key: 'create' });
        setCreateLoading(false);
        setPathModalVisible(true);
        return;
      }

      // 生成项目逻辑...
      const formData = form.getFieldsValue();
      
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

      const hasEnabledComponents = Object.values(config).some((item: any) => item.enabled);
      if (!hasEnabledComponents) {
        config.audio = { enabled: true, config: { duration: '5s', volume: 0.6 } };
        config.video = { enabled: true, config: { duration: '4.2s' } };
        config.text = { enabled: true, config: { text: '默认项目', duration: '3s' } };
        message.info('未启用组件，使用默认配置创建项目');
      }

      console.log('下载补丁包 - 使用配置:', config);

      const projectResult = await apiService.createComprehensiveProject(config);

      if (!projectResult.success) {
        throw new Error(projectResult.message || '创建项目失败');
      }

      setCurrentProjectData(projectResult.data);
      message.success({ content: '项目创建成功，请选择工程目录', key: 'create' });
      setCreateLoading(false);
      
      setPathModalVisible(true);

    } catch (error: any) {
      console.error('项目创建失败:', error);
      message.error({ content: `项目创建失败: ${error.message}`, key: 'create' });
      setCreateLoading(false);
    }
  };

  const handlePathConfirm = async (projectDir: string) => {
    if (!currentProjectData) {
      message.error('没有项目数据，请重新创建项目');
      setPathModalVisible(false);
      return;
    }

    try {
      setDownloadLoading(true);
      message.loading({ content: '正在保存项目...', key: 'download' });

      // 桌面版：直接保存到本地
      if (window.electronAPI) {
        // 保存 JSON 文件
        const jsonContent = JSON.stringify(currentProjectData, null, 2);
        const result = await window.electronAPI.saveFile(
          'draft_content.json',
          jsonContent
        );

        if (result.success) {
          message.success({ 
            content: '项目文件保存成功！', 
            key: 'download',
            duration: 5
          });

          // 显示成功信息
          Modal.success({
            title: '🎉 项目保存成功',
            width: 600,
            content: (
              <div style={{ marginTop: 16 }}>
                <div style={{ marginBottom: 12 }}>
                  <Text strong>保存位置:</Text>
                  <div style={{ 
                    background: '#f6ffed', 
                    padding: '8px', 
                    borderRadius: '4px', 
                    marginTop: '4px',
                    fontSize: '12px',
                    fontFamily: 'monospace'
                  }}>
                    {result.path}
                  </div>
                </div>
                
                <Alert
                  message="桌面版特性"
                  description="项目文件已保存到本地，您可以直接将其复制到剪映草稿目录使用。"
                  type="success"
                  showIcon
                  style={{ marginTop: 12 }}
                />
              </div>
            ),
            onOk: () => {
              setPathModalVisible(false);
              setDownloadLoading(false);
            }
          });

          // 桌面版通知
          window.electronAPI.showNotification(
            '剪映助手',
            '项目文件保存成功！'
          );
        } else {
          throw new Error(result.error || '保存失败');
        }
      } else {
        throw new Error('桌面版功能不可用');
      }

    } catch (error: any) {
      console.error('保存失败:', error);
      message.error({ content: `保存失败: ${error.message}`, key: 'download' });
      setDownloadLoading(false);
    }
  };

  const handlePathCancel = () => {
    setPathModalVisible(false);
    setCurrentProjectData(null);
  };

  const sectionConfigs = [
    {
      key: 'text',
      title: '文本片段',
      icon: <FontSizeOutlined />,
      color: '#1890ff',
      description: '添加文字内容和样式',
      fields: [
        { name: 'text', label: '文本内容', type: 'textarea', default: '桌面版测试文本' },
        { name: 'duration', label: '显示时长', type: 'input', default: '3s' },
        { name: 'font', label: '字体', type: 'select', options: ['文轩体', '思源黑体', '微软雅黑'] },
        { name: 'color', label: '文字颜色', type: 'color', default: [1.0, 1.0, 1.0] },
      ]
    },
    {
      key: 'audio',
      title: '音频设置',
      icon: <AudioOutlined />,
      color: '#52c41a',
      description: '配置音频片段参数',
      fields: [
        { name: 'duration', label: '时长', type: 'input', default: '5s' },
        { name: 'volume', label: '音量', type: 'number', min: 0, max: 1, step: 0.1, default: 0.6 },
        { name: 'fade_in', label: '淡入时长', type: 'input', default: '1s' },
      ]
    },
    {
      key: 'video',
      title: '视频设置',
      icon: <VideoCameraOutlined />,
      color: '#fa541c',
      description: '配置视频片段参数',
      fields: [
        { name: 'duration', label: '时长', type: 'input', default: '4.2s' },
      ]
    },
    {
      key: 'animation',
      title: '动画效果',
      icon: <ThunderboltOutlined />,
      color: '#722ed1',
      description: '为片段添加动画效果',
      fields: [
        { name: 'type', label: '动画类型', type: 'select', options: ['淡入', '淡出', '滑入', '滑出'], default: '淡入' },
        { name: 'duration', label: '持续时长', type: 'input', default: '1s' },
      ]
    },
    {
      key: 'effects',
      title: '视频特效',
      icon: <BgColorsOutlined />,
      color: '#13c2c2',
      description: '为视频添加特效',
      fields: [
        { name: 'type', label: '特效类型', type: 'select', options: ['无', '马赛克', '模糊', '锐化'], default: '无' },
        { name: 'intensity', label: '特效强度', type: 'number', min: 0, max: 100, step: 1, default: 50 },
      ]
    },
    {
      key: 'transition',
      title: '转场效果',
      icon: <FileTextOutlined />,
      color: '#fadb14',
      description: '设置片段之间的转场效果',
      fields: [
        { name: 'type', label: '转场类型', type: 'select', options: ['无', '溶解', '滑动', '翻页'], default: '无' },
        { name: 'duration', label: '持续时长', type: 'input', default: '1s' },
      ]
    },
  ];

  const renderField = (field: any) => {
    switch (field.type) {
      case 'textarea':
        return <TextArea rows={3} />;
      case 'select':
        return (
          <Select>
            {field.options?.map((option: string) => (
              <Option key={option} value={option}>{option}</Option>
            ))}
          </Select>
        );
      case 'number':
        return (
          <InputNumber 
            min={field.min} 
            max={field.max} 
            step={field.step}
            style={{ width: '100%' }}
          />
        );
      case 'color':
        return <ColorPicker />;
      case 'upload-audio':
      case 'upload-video':
        const type = field.type === 'upload-audio' ? 'audio' : 'video';
        const currentAsset = uploadedAssets.find(item => item.type === type);
        
        return currentAsset ? (
          <div style={{ 
            padding: '8px 12px', 
            background: type === 'audio' ? '#f6ffed' : '#fff7e6', 
            border: `1px solid ${type === 'audio' ? '#b7eb8f' : '#ffd591'}`,
            borderRadius: '6px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <span style={{ color: type === 'audio' ? '#52c41a' : '#fa8c16' }}>
              {type === 'audio' ? '🎵' : '🎬'} {currentAsset.filename}
            </span>
            <Button 
              type="text" 
              size="small" 
              icon={<DeleteOutlined />}
              onClick={() => removeAsset(type)}
            />
          </div>
        ) : (
          <Upload
            beforeUpload={(file) => handleFileUpload(file, type)}
            accept={`${type}/*`}
            showUploadList={false}
          >
            <Button icon={<UploadOutlined />} style={{ width: '100%' }}>
              选择本地{type === 'audio' ? '音频' : '视频'}文件
            </Button>
          </Upload>
        );
      default:
        return <Input />;
    }
  };

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
                  {renderField(field)}
                </Form.Item>
              </Col>
            ))}
          </Row>
        )}
      </div>
    ),
  }));

  return (
    <div className="create-project">
      <div style={{ marginBottom: '24px' }}>
        <Title level={2}>
          <Space>
            <Film size={32} color="#1890ff" />
            开始创作 - 桌面版
          </Space>
        </Title>
        <Paragraph type="secondary">
          桌面版提供本地文件访问和更快的响应速度。配置多媒体组件，一键生成综合剪映项目。
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
          <Card title="🖥️ 桌面版控制台" size="small">
            <Space direction="vertical" style={{ width: '100%' }} size={8}>
              <div>
                <Text strong>已启用组件:</Text>
                <Row gutter={[8, 4]} style={{ marginTop: 4 }}>
                  {Object.entries(projectData).map(([key, section]) => (
                    <Col span={12} key={key}>
                      <Checkbox 
                        checked={section.enabled} 
                        onChange={(e) => handleSectionToggle(key as keyof ProjectData, e.target.checked)}
                        style={{ fontSize: '12px' }}
                      >
                        <Text style={{ 
                          fontSize: '12px', 
                          color: section.enabled ? '#1890ff' : '#999' 
                        }}>
                          {sectionConfigs.find(s => s.key === key)?.title}
                        </Text>
                      </Checkbox>
                    </Col>
                  ))}
                </Row>
              </div>

              {uploadedAssets.length > 0 && (
                <div>
                  <Text strong>已上传素材:</Text>
                  <div style={{ 
                    display: 'flex', 
                    flexWrap: 'wrap', 
                    gap: '4px',
                    marginTop: 4
                  }}>
                    {uploadedAssets.map((asset, index) => (
                      <Tag 
                        key={index}
                        color={asset.type === 'audio' ? 'green' : 'blue'}
                        style={{ margin: '0', fontSize: '11px' }}
                      >
                        {asset.type === 'audio' ? '🎵' : '🎬'} {asset.filename.length > 15 ? asset.filename.substring(0, 12) + '...' : asset.filename}
                      </Tag>
                    ))}
                  </div>
                </div>
              )}

              <Alert
                message="桌面版特性: 本地文件访问 | 系统通知 | 快速保存"
                type="info"
                showIcon
                style={{ padding: '6px 10px', margin: '0' }}
              />

              <Button
                type="primary"
                size="middle"
                icon={<PlusOutlined />}
                loading={generateMutation.isPending}
                onClick={handleGenerate}
                block
                style={{ marginTop: 8 }}
              >
                {generateMutation.isPending ? '生成中...' : '生成集成项目'}
              </Button>

              <Button
                type="dashed"
                size="middle"
                icon={<FolderOpenOutlined />}
                loading={createLoading || downloadLoading}
                onClick={handleDownloadPatch}
                block
                style={{ marginTop: 4 }}
              >
                {(createLoading || downloadLoading) ? '处理中...' : '💾 保存到本地'}
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
            key="save"
            onClick={async () => {
              if (window.electronAPI && generatedResult) {
                const result = await window.electronAPI.saveFile(
                  `draft_content_${Date.now()}.json`,
                  JSON.stringify(generatedResult.data, null, 2)
                );
                if (result.success) {
                  message.success(`文件已保存到: ${result.path}`);
                } else {
                  message.error(`保存失败: ${result.error}`);
                }
              }
            }}
          >
            💾 保存文件
          </Button>,
        ]}
        width={900}
        destroyOnClose
      >
        {generatedResult ? (
          <div style={{ height: "400px" }}>
            <Editor
              height="100%"
              defaultLanguage="json"
              value={JSON.stringify(generatedResult.data || generatedResult, null, 2)}
              options={{
                readOnly: true,
                minimap: { enabled: false },
                fontSize: 12,
                theme: "vs-light",
                wordWrap: "on",
              }}
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

      {/* 路径选择弹窗 */}
      <PathSelectModal
        visible={pathModalVisible}
        onCancel={handlePathCancel}
        onConfirm={handlePathConfirm}
        loading={downloadLoading}
      />
    </div>
  );
};

export default CreateProject;