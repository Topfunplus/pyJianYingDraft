import React, { useState } from 'react';
import { Modal, Input, Select, Form, message, Button, Typography, Card } from 'antd';
import { FolderOpenOutlined, DownloadOutlined } from '@ant-design/icons';

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
  const [projectDir, setProjectDir] = useState('C:/Users/Default/Desktop/剪映项目');

  const examplePaths = [
    { label: '桌面/剪映项目', value: 'C:/Users/%USERNAME%/Desktop/剪映项目' },
    { label: 'D盘/剪映工程/我的项目', value: 'D:/剪映工程/我的项目' },
    { label: 'C盘/JianYing/Projects', value: 'C:/JianYing/Projects' },
  ];

  const handleExampleSelect = (value: string) => {
    setProjectDir(value);
    form.setFieldsValue({ projectDir: value });
  };

  const handleConfirm = async () => {
    try {
      const values = await form.validateFields();
      const dir = values.projectDir?.trim();
      
      if (!dir) {
        message.error('请输入工程目录路径');
        return;
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
      width={600}
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
          确定下载
        </Button>,
      ]}
    >
      <div style={{ marginBottom: 16 }}>
        <Card size="small" style={{ backgroundColor: '#f6ffed', border: '1px solid #b7eb8f' }}>
          <Text type="secondary">
            📁 请选择您希望存放剪映素材的目录路径。所有音视频素材将保存在此目录的 assets 子文件夹中。
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
          <Input
            placeholder="例如: C:/Users/用户名/Desktop/剪映项目"
            value={projectDir}
            onChange={(e) => setProjectDir(e.target.value)}
            size="large"
          />
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
                {path.label}
              </Option>
            ))}
          </Select>
        </Form.Item>
      </Form>

      <div style={{ marginTop: 16 }}>
        <Card size="small" style={{ backgroundColor: '#fff7e6', border: '1px solid #ffd591' }}>
          <Title level={5} style={{ margin: 0, marginBottom: 8 }}>
            📋 使用说明
          </Title>
          <div style={{ fontSize: '12px', color: '#666' }}>
            <div>1. 系统将自动配置所有素材的绝对路径</div>
            <div>2. 下载后将素材文件放到 {projectDir}/assets/ 目录</div>
            <div>3. 将 draft_content.json 导入剪映即可使用</div>
            <div>4. 确保剪映有权限访问该目录</div>
          </div>
        </Card>
      </div>
    </Modal>
  );
};

export default PathSelectModal;
