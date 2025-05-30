import React, { useState } from 'react';
import { 
  Card, Form, Input, Button, Select, Space, Typography, Row, Col, 
  Checkbox, InputNumber, ColorPicker, Tabs, Alert, Spin, Modal, message, List, Upload
} from 'antd';
import { useMutation } from '@tanstack/react-query';
import { 
  PlusOutlined, PlayCircleOutlined, FileTextOutlined, 
  AudioOutlined, VideoCameraOutlined, FontSizeOutlined,
  ThunderboltOutlined, BgColorsOutlined, UploadOutlined, DeleteOutlined,
  DownloadOutlined  // 添加缺失的图标导入
} from '@ant-design/icons';
import { Film, Sparkles } from 'lucide-react';
import Editor from '@monaco-editor/react';
import { apiService } from '@/services/api';
import PathSelectModal from '@/components/PathSelectModal';

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
  const [downloadUrl, setDownloadUrl] = useState<{audio?: string, video?: string}>({});
  const [downloading, setDownloading] = useState<{audio?: boolean, video?: boolean}>({});
  const [pathModalVisible, setPathModalVisible] = useState(false);
  const [currentProjectData, setCurrentProjectData] = useState<any>(null);
  const [downloadLoading, setDownloadLoading] = useState(false);
  // 添加缺失的状态变量
  const [createLoading, setCreateLoading] = useState(false);

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

  const handleUrlDownload = async (url: string, type: 'audio' | 'video') => {
    if (!url.trim()) {
      message.error('请输入有效的网址');
      return;
    }

    setDownloading(prev => ({ ...prev, [type]: true }));
    
    try {
      const response = await fetch('/api/download-from-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, type })
      });

      if (response.ok) {
        const result = await response.json();
        const asset: UploadedAsset = {
          filename: result.filename,
          type,
          source: 'download',
          size: result.size
        };
        
        setUploadedAssets(prev => [
          ...prev.filter(item => item.type !== type),
          asset
        ]);
        
        setDownloadUrl(prev => ({ ...prev, [type]: '' }));
        message.success(`${type === 'audio' ? '音频' : '视频'}文件下载成功`);
      } else {
        const errorData = await response.json();
        message.error(`下载失败: ${errorData.message}`);
      }
    } catch (error) {
      message.error(`下载失败: ${error}`);
    } finally {
      setDownloading(prev => ({ ...prev, [type]: false }));
    }
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

      // 检查是否已有生成的项目数据
      if (generatedResult?.data) {
        // 如果已有项目数据，直接使用
        setCurrentProjectData(generatedResult.data);
        message.success({ content: '使用当前项目数据，请选择工程目录', key: 'create' });
        setCreateLoading(false);
        setPathModalVisible(true);
        return;
      }

      // 如果没有项目数据，需要先生成项目
      const formData = form.getFieldsValue();
      
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

      // 检查是否有启用的组件，如果没有则使用默认配置
      const hasEnabledComponents = Object.values(config).some((item: any) => item.enabled);
      if (!hasEnabledComponents) {
        // 使用默认配置
        config.audio = { enabled: true, config: { duration: '5s', volume: 0.6 } };
        config.video = { enabled: true, config: { duration: '4.2s' } };
        config.text = { enabled: true, config: { text: '默认项目', duration: '3s' } };
        message.info('未启用组件，使用默认配置创建项目');
      }

      console.log('下载补丁包 - 使用配置:', config);

      // 创建项目
      const projectResponse = await fetch('/api/comprehensive-create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });

      if (!projectResponse.ok) {
        const errorData = await projectResponse.json();
        throw new Error(errorData.message || '创建项目失败');
      }

      const projectResult = await projectResponse.json();
      setCurrentProjectData(projectResult.data);

      message.success({ content: '项目创建成功，请选择工程目录', key: 'create' });
      setCreateLoading(false);
      
      // 显示路径选择弹窗
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
      message.loading({ content: '正在配置路径...', key: 'download' });

      // 第一步：配置路径
      const configResponse = await fetch('/api/select-project-dir', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_data: currentProjectData,
          project_dir: projectDir
        })
      });

      if (!configResponse.ok) {
        const errorResult = await configResponse.json();
        throw new Error(errorResult.message || '路径配置失败');
      }

      const configResult = await configResponse.json();
      
      message.loading({ content: '正在生成并保存补丁包...', key: 'download' });

      // 第二步：生成并保存补丁包到指定目录
      const downloadResponse = await fetch('/api/download-patch-simple', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_data: configResult.data,
          project_dir: projectDir
        })
      });

      if (!downloadResponse.ok) {
        const errorResult = await downloadResponse.json();
        throw new Error(errorResult.message || '保存失败');
      }

      // 获取保存结果
      const result = await downloadResponse.json();
      
      message.success({ 
        content: '补丁包已成功保存到指定目录！', 
        key: 'download',
        duration: 8
      });

      // 显示详细的保存信息
      Modal.success({
        title: '🎉 补丁包保存成功',
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
                {result.details?.full_path}
              </div>
            </div>
            
            <div style={{ marginBottom: 12 }}>
              <Text strong>包含内容:</Text>
              <ul style={{ marginTop: '4px', fontSize: '14px' }}>
                <li>📄 draft_content.json - 剪映项目文件</li>
                <li>📁 assets/ - 素材文件目录 ({result.details?.assets_count} 个文件)</li>
                <li>📋 README.md - 使用说明</li>
                <li>📦 {result.details?.zip_file} - 完整补丁包</li>
              </ul>
            </div>

            <div style={{ marginBottom: 12 }}>
              <Text strong>下一步操作:</Text>
              <ol style={{ marginTop: '4px', fontSize: '14px' }}>
                <li>素材文件已自动放置在正确位置</li>
                <li>将 draft_content.json 复制到剪映草稿目录</li>
                <li>在剪映中打开项目即可使用</li>
              </ol>
            </div>

            <Alert
              message="提示"
              description={`所有文件已准备完毕，项目可以在剪映中直接使用。ZIP文件可用于备份或分享。`}
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
      description: '配置音频参数并上传音频文件',
      fields: [
        { name: 'duration', label: '音频时长', type: 'input', default: '5s' },
        { name: 'volume', label: '音量大小', type: 'number', default: 0.6, min: 0, max: 1, step: 0.1 },
        { name: 'fade_in', label: '淡入时间', type: 'input', default: '1s' },
        { name: 'upload', label: '上传音频', type: 'upload-audio' },
      ]
    },
    {
      key: 'video',
      title: '视频片段',
      icon: <VideoCameraOutlined />,
      color: '#fa8c16',
      description: '设置视频参数并上传视频文件',
      fields: [
        { name: 'duration', label: '视频时长', type: 'input', default: '4.2s' },
        { name: 'upload', label: '上传视频', type: 'upload-video' },
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
        return (
          <div>
            {uploadedAssets.find(item => item.type === 'audio') ? (
              <div style={{ 
                padding: '8px 12px', 
                background: '#f6ffed', 
                border: '1px solid #b7eb8f',
                borderRadius: '6px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <span style={{ color: '#52c41a' }}>
                  🎵 {uploadedAssets.find(item => item.type === 'audio')?.filename}
                  {uploadedAssets.find(item => item.type === 'audio')?.source === 'download' && 
                    <span style={{ fontSize: '12px', marginLeft: '8px', opacity: 0.7 }}>(网络下载)</span>
                  }
                </span>
                <Button 
                  type="text" 
                  size="small" 
                  icon={<DeleteOutlined />}
                  onClick={() => removeAsset('audio')}
                />
              </div>
            ) : (
              <div>
                <div style={{ marginBottom: '8px' }}>
                  <Upload
                    beforeUpload={(file) => handleFileUpload(file, 'audio')}
                    accept="audio/*"
                    showUploadList={false}
                  >
                    <Button icon={<UploadOutlined />} style={{ width: '100%' }}>
                      选择本地音频文件
                    </Button>
                  </Upload>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <Input
                    placeholder="输入音频网址"
                    value={downloadUrl.audio || ''}
                    onChange={(e) => setDownloadUrl(prev => ({ ...prev, audio: e.target.value }))}
                    style={{ flex: 1 }}
                  />
                  <Button
                    loading={downloading.audio}
                    onClick={() => handleUrlDownload(downloadUrl.audio || '', 'audio')}
                    disabled={!downloadUrl.audio?.trim()}
                  >
                    下载
                  </Button>
                </div>
              </div>
            )}
          </div>
        );
      case 'upload-video':
        return (
          <div>
            {uploadedAssets.find(item => item.type === 'video') ? (
              <div style={{ 
                padding: '8px 12px', 
                background: '#fff7e6', 
                border: '1px solid #ffd591',
                borderRadius: '6px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <span style={{ color: '#fa8c16' }}>
                  🎬 {uploadedAssets.find(item => item.type === 'video')?.filename}
                  {uploadedAssets.find(item => item.type === 'video')?.source === 'download' && 
                    <span style={{ fontSize: '12px', marginLeft: '8px', opacity: 0.7 }}>(网络下载)</span>
                  }
                </span>
                <Button 
                  type="text" 
                  size="small" 
                  icon={<DeleteOutlined />}
                  onClick={() => removeAsset('video')}
                />
              </div>
            ) : (
              <div>
                <div style={{ marginBottom: '8px' }}>
                  <Upload
                    beforeUpload={(file) => handleFileUpload(file, 'video')}
                    accept="video/*"
                    showUploadList={false}
                  >
                    <Button icon={<UploadOutlined />} style={{ width: '100%' }}>
                      选择本地视频文件
                    </Button>
                  </Upload>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <Input
                    placeholder="输入视频网址"
                    value={downloadUrl.video || ''}
                    onChange={(e) => setDownloadUrl(prev => ({ ...prev, video: e.target.value }))}
                    style={{ flex: 1 }}
                  />
                  <Button
                    loading={downloading.video}
                    onClick={() => handleUrlDownload(downloadUrl.video || '', 'video')}
                    disabled={!downloadUrl.video?.trim()}
                  >
                    下载
                  </Button>
                </div>
              </div>
            )}
          </div>
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

              {uploadedAssets.length > 0 && (
                <div>
                  <Text strong>已上传素材:</Text>
                  <div style={{ marginTop: 8 }}>
                    {uploadedAssets.map((asset, index) => (
                      <div key={index} style={{ 
                        fontSize: '12px', 
                        color: '#666',
                        marginBottom: '4px'
                      }}>
                        {asset.type === 'audio' ? '🎵' : '🎬'} {asset.filename}
                        <span style={{ opacity: 0.7, marginLeft: '4px' }}>
                          ({asset.source === 'upload' ? '本地上传' : '网络下载'})
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

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

              {/* 添加独立的下载补丁包按钮 */}
              <Button
                type="dashed"
                size="large"
                icon={<DownloadOutlined />}
                loading={createLoading || downloadLoading}
                onClick={handleDownloadPatch}
                block
                style={{ marginTop: 8 }}
                disabled={createLoading || downloadLoading}
              >
                {(createLoading || downloadLoading) ? '处理中...' : '📦 直接下载补丁包'}
              </Button>

              <Alert
                message="下载说明"
                description="可以直接下载补丁包，系统会根据当前配置自动生成项目。如果未配置组件，将使用默认模板。"
                type="info"
                showIcon
                style={{ marginTop: 8 }}
              />

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
            key="download-json"
            onClick={() => {
              if (generatedResult) {
                const blob = new Blob([JSON.stringify(generatedResult.data, null, 2)], {
                  type: 'application/json'
                });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `draft_content_${Date.now()}.json`;
                a.click();
                URL.revokeObjectURL(url);
                message.success('JSON文件下载完成');
              }
            }}
          >
            下载JSON
          </Button>,
          <Button
            key="download-patch"
            type="dashed"
            onClick={handleDownloadPatch}
            loading={createLoading || downloadLoading}
            icon={<DownloadOutlined />}
          >
            📦 下载完整补丁包
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
                                    {item.file_exists !== undefined && (
                                      <div style={{ color: item.file_exists ? '#52c41a' : '#faad14' }}>
                                        素材状态: {item.file_exists ? '✅ 文件存在' : '⚠️ 需要素材文件'}
                                      </div>
                                    )}
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
                },
                {
                  key: 'assets',
                  label: '素材文件',
                  children: (
                    <div style={{ height: '400px', overflow: 'auto' }}>
                      {(uploadedAssets.length > 0 || generatedResult.summary?.assets?.length > 0) ? (
                        <div>
                          <Alert
                            message="素材文件说明"
                            description="以下是项目所需的素材文件，下载补丁包将包含这些文件。"
                            type="info"
                            showIcon
                            style={{ marginBottom: 16 }}
                          />
                          
                          {/* 用户上传的素材 */}
                          {uploadedAssets.length > 0 && (
                            <div style={{ marginBottom: 16 }}>
                              <Text strong style={{ color: '#1890ff' }}>用户素材:</Text>
                              <List
                                size="small"
                                dataSource={uploadedAssets}
                                renderItem={(asset: UploadedAsset) => (
                                  <List.Item>
                                    <List.Item.Meta
                                      title={
                                        <Space>
                                          <span>{asset.filename}</span>
                                          <span style={{ 
                                            fontSize: '12px', 
                                            padding: '2px 6px', 
                                            borderRadius: '4px',
                                            backgroundColor: asset.type === 'video' ? '#1890ff' : '#52c41a',
                                            color: 'white'
                                          }}>
                                            {asset.type}
                                          </span>
                                          <span style={{ 
                                            fontSize: '12px', 
                                            padding: '2px 6px', 
                                            borderRadius: '4px',
                                            backgroundColor: asset.source === 'upload' ? '#52c41a' : '#fa8c16',
                                            color: 'white'
                                          }}>
                                            {asset.source === 'upload' ? '本地' : '网络'}
                                          </span>
                                        </Space>
                                      }
                                      description={
                                        <div>
                                          {asset.size && <div>文件大小: {(asset.size / (1024 * 1024)).toFixed(2)} MB</div>}
                                          <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
                                            来源: {asset.source === 'upload' ? '用户上传' : '网络下载'}的{asset.type === 'audio' ? '音频' : '视频'}文件
                                          </div>
                                        </div>
                                      }
                                    />
                                  </List.Item>
                                )}
                              />
                            </div>
                          )}
                          
                          {/* 系统默认素材 */}
                          {generatedResult.summary?.assets?.length > 0 && (
                            <div>
                              <Text strong style={{ color: '#666' }}>系统默认素材:</Text>
                              <List
                                size="small"
                                dataSource={generatedResult.summary.assets}
                                renderItem={(asset: any) => (
                                  <List.Item>
                                    <List.Item.Meta
                                      title={
                                        <Space>
                                          <span>{asset.filename}</span>
                                          <span style={{ 
                                            fontSize: '12px', 
                                            padding: '2px 6px', 
                                            borderRadius: '4px',
                                            backgroundColor: '#666',
                                            color: 'white'
                                          }}>
                                            {asset.type}
                                          </span>
                                        </Space>
                                      }
                                      description={
                                        <div>
                                          <div>{asset.description}</div>
                                          <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
                                            路径: {asset.path}
                                          </div>
                                        </div>
                                      }
                                    />
                                  </List.Item>
                                )}
                              />
                            </div>
                          )}
                          
                          <div style={{ marginTop: 16, textAlign: 'center' }}>
                            <Button type="primary" onClick={handleDownloadPatch}>
                              📦 下载完整补丁包
                            </Button>
                          </div>
                        </div>
                      ) : (
                        <div style={{ textAlign: 'center', padding: '20px' }}>
                          <Text type="secondary">当前项目无需素材文件</Text>
                          <br />
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            请在相应组件中上传音视频文件，或启用需要素材的组件
                          </Text>
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
