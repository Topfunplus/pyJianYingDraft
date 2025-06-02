import React, { useState } from 'react';
import { Modal, Input, Select, Form, message, Button, Typography, Card, Space } from 'antd';
import { FolderOpenOutlined, DownloadOutlined, FolderOutlined } from '@ant-design/icons';

const { Text, Title } = Typography;
const { Option } = Select;

interface PathSelectModalProps {
  visible: boolean;
  onCancel: () => void;
  onConfirm: (projectDir: string) => Promise<void>;
  loading?: boolean;
}

const PathSelectModal: React.FC<PathSelectModalProps> = ({
  visible,
  onCancel,
  onConfirm,
  loading = false
}) => {
  const [form] = Form.useForm();
  const [projectDir, setProjectDir] = useState('C:/Users/Desktop/剪映项目');

  const examplePaths = [
    { label: '桌面/剪映项目', value: 'C:/Users/Desktop/剪映项目' },
    { label: 'D盘/剪映工程/我的项目', value: 'D:/剪映工程/我的项目' },
    { label: 'C盘/JianYing/Projects', value: 'C:/JianYing/Projects' },
    { label: '文档/剪映作品', value: 'C:/Users/Documents/剪映作品' },
  ];

  const handleExampleSelect = (value: string) => {
    setProjectDir(value);
    form.setFieldsValue({ projectDir: value });
  };

  const handleSelectDirectory = async () => {
    if (window.electronAPI) {
      const selectedPath = await window.electronAPI.selectDirectory();
      if (selectedPath) {
        setProjectDir(selectedPath);
        form.setFieldsValue({ projectDir: selectedPath });
      }
    } else {
      message.info('桌面版功能，请在桌面应用中使用');
    }
  };

  const handleConfirm = async () => {
    try {
      const values = await form.validateFields();
      const dir = values.projectDir?.trim();
      
      if (!dir) {
        message.error('请输入工程目录路径');
        return;
      }

      // 桌面版：检查目录是否存在，不存在则创建
      if (window.electronAPI) {
        const exists = await window.electronAPI.checkDirectory(dir);
        if (!exists) {
          const result = await window.electronAPI.createDirectory(dir);
          if (!result.success) {
            message.error(`创建目录失败: ${result.error}`);
            return;
          }
          message.success('目录创建成功');
        }
      }

      await onConfirm(dir);
    } catch (error) {
      console.error('路径选择失败:', error);
    }
  };

  return (
    <Modal
      title={
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <FolderOpenOutlined style={{ color: '#1890ff' }} />
          <span>选择剪映工程目录</span>
        </div>
      }
      open={visible}
      onCancel={onCancel}
      width={700}
      footer={[
        <Button key="cancel" onClick={onCancel} disabled={loading}>
          取消
        </Button>,
        <Button
          key="confirm"
          type="primary"
          onClick={handleConfirm}
          loading={loading}
          icon={<DownloadOutlined />}
        >
          确定保存到此目录
        </Button>,
      ]}
    >
      <div style={{ marginBottom: 16 }}>
        <Card size="small" style={{ backgroundColor: '#f6ffed', border: '1px solid #b7eb8f' }}>
          <Text type="secondary">
            📁 请选择您希望保存剪映项目的目录路径。系统将直接在此目录创建项目文件和素材文件夹。
          </Text>
        </Card>
      </div>

      <Form
        form={form}
        layout="vertical"
        initialValues={{ projectDir }}
      >
        <Form.Item
          label="工程目录路径"
          name="projectDir"
          rules={[
            { required: true, message: '请输入工程目录路径' },
            { min: 3, message: '路径长度至少3个字符' },
          ]}
        >
          <Input.Group compact>
            <Input
              style={{ width: 'calc(100% - 120px)' }}
              placeholder="例如: C:/Users/用户名/Desktop/剪映项目"
              value={projectDir}
              onChange={(e) => setProjectDir(e.target.value)}
              size="large"
            />
            <Button 
              type="primary" 
              onClick={handleSelectDirectory}
              icon={<FolderOutlined />}
              size="large"
              style={{ width: '120px' }}
            >
              浏览选择
            </Button>
          </Input.Group>
        </Form.Item>

        <Form.Item label="示例路径">
          <Select
            placeholder="选择示例路径"
            onChange={handleExampleSelect}
            size="large"
            allowClear
          >
            {examplePaths.map((path) => (
              <Option key={path.value} value={path.value}>
                <Space>
                  <FolderOutlined />
                  {path.label}
                </Space>
              </Option>
            ))}
          </Select>
        </Form.Item>
      </Form>

      <div style={{ marginTop: 16 }}>
        <Card size="small" style={{ backgroundColor: '#fff7e6', border: '1px solid #ffd591' }}>
          <Title level={5} style={{ margin: 0, marginBottom: 8 }}>
            📋 桌面版特性
          </Title>
          <div style={{ fontSize: '12px', color: '#666' }}>
            <div>1. 🗂️ 支持文件夹浏览器选择目录</div>
            <div>2. 📁 自动创建不存在的目录</div>
            <div>3. 💾 直接保存到本地文件系统</div>
            <div>4. 📦 生成完整的项目包和ZIP备份</div>
            <div>5. 🔔 操作完成后系统通知</div>
          </div>
        </Card>
      </div>
    </Modal>
  );
};

export default PathSelectModal;
