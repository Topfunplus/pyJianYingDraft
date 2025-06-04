import React, { useState } from "react";
import {
  Card,
  Form,
  Input,
  Button,
  Select,
  Space,
  Typography,
  Row,
  Col,
  Checkbox,
  InputNumber,
  ColorPicker,
  Alert,
  Spin,
  Modal,
  message,
  List,
  Upload,
  Steps,
  Divider,
  Tabs,
} from "antd";
import { useMutation } from "@tanstack/react-query";
import {
  PlusOutlined,
  PlayCircleOutlined,
  AudioOutlined,
  VideoCameraOutlined,
  FontSizeOutlined,
  ThunderboltOutlined,
  BgColorsOutlined,
  UploadOutlined,
  DeleteOutlined,
  CheckOutlined,
  ArrowLeftOutlined,
  ArrowRightOutlined,
} from "@ant-design/icons";
import { Film, Sparkles, Settings } from "lucide-react";
import Editor from "@monaco-editor/react";
import { apiService } from "@/services/api";
import PathSelectModal from "@/components/PathSelectModal";

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { TextArea } = Input;
const { Step } = Steps;

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
  type: "audio" | "video";
  url?: string;
  source: "upload";
  size?: number;
}

const CreateProject: React.FC = () => {
  const [form] = Form.useForm();
  const [configModalVisible, setConfigModalVisible] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [projectData, setProjectData] = useState<ProjectData>({
    text: { enabled: false, config: {} },
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
  const [createLoading, setCreateLoading] = useState(false);

  // 综合项目生成mutation
  const generateMutation = useMutation({
    mutationFn: async (config: any) => {
      console.log("开始调用API，配置:", config);
      try {
        // 调用新的综合创作API
        const result = await apiService.createComprehensiveProject(config);
        console.log("API调用成功:", result);
        return result;
      } catch (error) {
        console.error("API调用失败:", error);
        throw error;
      }
    },
    onSuccess: (data) => {
      console.log("项目生成成功:", data);
      setGeneratedResult(data);
      setConfigModalVisible(false);
      setPreviewVisible(true);
      message.success("项目生成成功！");
    },
    onError: (error: any) => {
      console.error("项目生成失败:", error);
      // 显示更详细的错误信息
      const errorMessage =
        error?.response?.data?.message || error?.message || "未知错误";
      message.error(`项目生成失败: ${errorMessage}`);
    },
  });

  const handleSectionToggle = (
    section: keyof ProjectData,
    enabled: boolean
  ) => {
    setProjectData((prev) => ({
      ...prev,
      [section]: { ...prev[section], enabled },
    }));
  };

  const handleFileUpload = (file: File, type: "audio" | "video") => {
    const url = URL.createObjectURL(file);
    const asset: UploadedAsset = {
      file,
      filename: file.name,
      type,
      url,
      source: "upload",
      size: file.size,
    };

    setUploadedAssets((prev) => [
      ...prev.filter((item) => item.type !== type),
      asset,
    ]);

    message.success(`${type === "audio" ? "音频" : "视频"}文件上传成功`);
    return false;
  };

  const removeAsset = (type: "audio" | "video") => {
    setUploadedAssets((prev) => {
      const removed = prev.find((item) => item.type === type);
      if (removed?.url) {
        URL.revokeObjectURL(removed.url);
      }
      return prev.filter((item) => item.type !== type);
    });
    message.success(`${type === "audio" ? "音频" : "视频"}文件已移除`);
  };

  const handleGenerate = () => {
    try {
      console.log("开始生成项目...");
      const formData = form.getFieldsValue();
      console.log("表单数据:", formData);
      console.log("项目状态:", projectData);

      // 构建配置对象
      const config: any = {};
      Object.keys(projectData).forEach((key) => {
        const section = projectData[key as keyof ProjectData];
        config[key] = {
          enabled: section.enabled,
          config: {
            ...section.config,
            ...(formData[key] || {}),
          },
        };
      });

      // 检查是否有启用的组件
      const hasEnabledComponents = Object.values(config).some(
        (item: any) => item.enabled
      );
      if (!hasEnabledComponents) {
        message.warning("请至少启用一个组件");
        return;
      }
      generateMutation.mutate(config);
    } catch (error) {
      console.error("配置生成失败:", error);
      message.error("配置生成失败，请检查输入参数");
    }
  };

  const handleDownloadPatch = async () => {
    try {
      setCreateLoading(true);
      message.loading({ content: "正在准备项目数据...", key: "create" });

      // 检查是否已有生成的项目数据
      if (generatedResult?.data) {
        // 如果已有项目数据，直接使用
        setCurrentProjectData(generatedResult.data);
        message.success({
          content: "使用当前项目数据，请选择工程目录",
          key: "create",
        });
        setCreateLoading(false);
        setPathModalVisible(true);
        return;
      }

      // 如果没有项目数据，需要先生成项目
      const formData = form.getFieldsValue();

      // 构建配置对象
      const config: any = {};
      Object.keys(projectData).forEach((key) => {
        const section = projectData[key as keyof ProjectData];
        config[key] = {
          enabled: section.enabled,
          config: {
            ...section.config,
            ...(formData[key] || {}),
          },
        };
      });

      // 检查是否有启用的组件，如果没有则使用默认配置
      const hasEnabledComponents = Object.values(config).some(
        (item: any) => item.enabled
      );
      if (!hasEnabledComponents) {
        // 使用默认配置
        config.audio = {
          enabled: true,
          config: { duration: "5s", volume: 0.6 },
        };
        config.video = { enabled: true, config: { duration: "4.2s" } };
        config.text = {
          enabled: true,
          config: { text: "默认项目", duration: "3s" },
        };
        message.info("未启用组件，使用默认配置创建项目");
      }

      console.log("下载补丁包 - 使用配置:", config);

      // 创建项目 - 改进错误处理
      const projectResponse = await fetch("/api/comprehensive-create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config),
      });

      // 检查响应状态
      if (!projectResponse.ok) {
        let errorMessage = `HTTP ${projectResponse.status}: ${projectResponse.statusText}`;
        try {
          const errorData = await projectResponse.text();
          const parsedError = JSON.parse(errorData);
          errorMessage = parsedError.message || errorMessage;
        } catch (parseError) {
          console.warn("无法解析错误响应:", parseError);
        }
        throw new Error(errorMessage);
      }

      // 尝试解析JSON响应
      let projectResult;
      try {
        const responseText = await projectResponse.text();
        console.log("API响应原始文本:", responseText);

        if (!responseText.trim()) {
          throw new Error("服务器返回空响应");
        }

        projectResult = JSON.parse(responseText);
      } catch (jsonError) {
        console.error("JSON解析失败:", jsonError);
        throw new Error("服务器响应格式错误，请检查后端服务");
      }

      if (!projectResult.success) {
        // 显示更友好的错误信息
        let errorMessage = projectResult.message || "创建项目失败";

        if (projectResult.user_tips?.suggestions) {
          errorMessage +=
            "\n\n建议：\n" + projectResult.user_tips.suggestions.join("\n");
        }

        throw new Error(errorMessage);
      }

      // 显示警告信息（如果有）
      if (projectResult.summary?.warnings?.length > 0) {
        message.warning({
          content: (
            <div>
              <div>项目创建成功，但有以下提示：</div>
              {projectResult.summary.warnings.map(
                (warning: string, index: number) => (
                  <div
                    key={index}
                    style={{ fontSize: "12px", marginTop: "4px" }}>
                    {warning}
                  </div>
                )
              )}
            </div>
          ),
          duration: 6,
          key: "warnings",
        });
      }

      // 显示用户提示
      if (projectResult.user_tips?.suggestions) {
        console.log("💡 用户提示:", projectResult.user_tips.suggestions);
      }

      setCurrentProjectData(projectResult.data);
      message.success({
        content: "项目创建成功，请选择工程目录",
        key: "create",
      });
      setCreateLoading(false);

      // 显示路径选择弹窗
      setPathModalVisible(true);
    } catch (error: any) {
      console.error("项目创建失败:", error);
      message.error({
        content: `项目创建失败: ${error.message}`,
        key: "create",
      });
      setCreateLoading(false);
    }
  };

  const handlePathConfirm = async (projectDir: string) => {
    if (!currentProjectData) {
      message.error("没有项目数据，请重新创建项目");
      setPathModalVisible(false);
      return;
    }

    try {
      // 第一步：配置路径
      const configResponse = await fetch("/api/select-project-dir", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_data: currentProjectData,
          project_dir: projectDir,
        }),
      });

      if (!configResponse.ok) {
        const errorResult = await configResponse.json();
        throw new Error(errorResult.message || "路径配置失败");
      }

      const configResult = await configResponse.json();

      // 第二步：生成并保存补丁包到指定目录
      const downloadResponse = await fetch("/api/download-patch-simple", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_data: configResult.data,
          project_dir: projectDir,
        }),
      });

      if (!downloadResponse.ok) {
        const errorResult = await downloadResponse.json();
        throw new Error(errorResult.message || "保存失败");
      }

      // 获取保存结果
      const result = await downloadResponse.json();

      message.success({
        content: "补丁包已成功保存到指定目录！",
        key: "download",
        duration: 8,
      });

      // 显示详细的保存信息
      Modal.success({
        title: "🎉 补丁包保存成功",
        width: 600,
        content: (
          <div style={{ marginTop: 16 }}>
            <div style={{ marginBottom: 12 }}>
              <Text strong>保存位置:</Text>
              <div
                style={{
                  background: "#f6ffed",
                  padding: "8px",
                  borderRadius: "4px",
                  marginTop: "4px",
                  fontSize: "12px",
                  fontFamily: "monospace",
                }}>
                {result.details?.full_path}
              </div>
            </div>

            <div style={{ marginBottom: 12 }}>
              <Text strong>包含内容:</Text>
              <ul style={{ marginTop: "4px", fontSize: "14px" }}>
                <li>📄 draft_content.json - 剪映项目文件</li>
                <li>
                  📁 assets/ - 素材文件目录 ({result.details?.assets_count}{" "}
                  个文件)
                </li>
                <li>📋 README.md - 使用说明</li>
                <li>📦 {result.details?.zip_file} - 完整补丁包</li>
              </ul>
            </div>

            <div style={{ marginBottom: 12 }}>
              <Text strong>下一步操作:</Text>
              <ol style={{ marginTop: "4px", fontSize: "14px" }}>
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
        },
      });
    } catch (error: any) {
      console.error("保存失败:", error);
      message.error({ content: `保存失败: ${error.message}`, key: "download" });
    }
  };

  const handlePathCancel = () => {
    setPathModalVisible(false);
    setCurrentProjectData(null);
  };

  const stepConfigs = [
    {
      key: "text",
      title: "文本片段",
      icon: <FontSizeOutlined />,
      color: "#1890ff",
      description: "添加文字内容和样式设置",
      fields: [
        {
          name: "text",
          label: "文本内容",
          type: "textarea",
          default: "欢迎使用剪映助手",
          required: true,
        },
        {
          name: "duration",
          label: "显示时长",
          type: "input",
          default: "3s",
          placeholder: "例如: 3s, 1.5s",
        },
        {
          name: "font",
          label: "字体",
          type: "select",
          options: ["文轩体", "思源黑体", "微软雅黑"],
          default: "文轩体",
        },
        {
          name: "color",
          label: "文字颜色",
          type: "color",
          default: [1.0, 1.0, 1.0],
        },
      ],
    },
    {
      key: "audio",
      title: "音频片段",
      icon: <AudioOutlined />,
      color: "#52c41a",
      description: "配置音频参数并上传音频文件",
      fields: [
        {
          name: "duration",
          label: "音频时长",
          type: "input",
          default: "5s",
          placeholder: "例如: 5s, 10s",
        },
        {
          name: "volume",
          label: "音量大小",
          type: "number",
          default: 0.6,
          min: 0,
          max: 1,
          step: 0.1,
        },
        {
          name: "fade_in",
          label: "淡入时间",
          type: "input",
          default: "1s",
          placeholder: "例如: 1s, 0.5s",
        },
        { name: "upload", label: "上传音频", type: "upload-audio" },
      ],
    },
    {
      key: "video",
      title: "视频片段",
      icon: <VideoCameraOutlined />,
      color: "#fa8c16",
      description: "设置视频参数并上传视频文件",
      fields: [
        {
          name: "duration",
          label: "视频时长",
          type: "input",
          default: "4.2s",
          placeholder: "例如: 4.2s, 6s",
        },
        { name: "upload", label: "上传视频", type: "upload-video" },
      ],
    },
    {
      key: "animation",
      title: "动画效果",
      icon: <ThunderboltOutlined />,
      color: "#eb2f96",
      description: "为文本添加动画特效",
      fields: [
        {
          name: "text",
          label: "动画文本",
          type: "input",
          default: "动画效果展示",
          placeholder: "输入要添加动画的文本",
        },
        {
          name: "animation_type",
          label: "动画类型",
          type: "select",
          options: ["渐显", "淡入", "弹跳", "故障闪动"],
          default: "故障闪动",
        },
        {
          name: "duration",
          label: "持续时间",
          type: "input",
          default: "2s",
          placeholder: "例如: 2s, 1s",
        },
      ],
    },
    {
      key: "effects",
      title: "文本特效",
      icon: <BgColorsOutlined />,
      color: "#722ed1",
      description: "添加气泡和花字等特效",
      fields: [
        {
          name: "text",
          label: "特效文本",
          type: "input",
          default: "特效文字",
          placeholder: "输入要添加特效的文本",
        },
        {
          name: "effect_type",
          label: "特效类型",
          type: "select",
          options: ["bubble", "flower"],
          default: "bubble",
        },
        {
          name: "duration",
          label: "显示时长",
          type: "input",
          default: "3s",
          placeholder: "例如: 3s, 5s",
        },
      ],
    },
    {
      key: "transition",
      title: "转场效果",
      icon: <PlayCircleOutlined />,
      color: "#13c2c2",
      description: "设置视频片段间的转场过渡",
      fields: [
        {
          name: "transition_type",
          label: "转场类型",
          type: "select",
          options: ["信号故障", "淡化", "滑动"],
          default: "信号故障",
        },
        {
          name: "segment1_duration",
          label: "前段时长",
          type: "input",
          default: "2s",
          placeholder: "例如: 2s",
        },
        {
          name: "segment2_duration",
          label: "后段时长",
          type: "input",
          default: "2s",
          placeholder: "例如: 2s",
        },
      ],
    },
  ];

  const renderField = (field: any) => {
    switch (field.type) {
      case "textarea":
        return <TextArea rows={3} placeholder={field.placeholder} />;
      case "select":
        return (
          <Select placeholder={`请选择${field.label}`}>
            {field.options?.map((option: string) => (
              <Option key={option} value={option}>
                {option}
              </Option>
            ))}
          </Select>
        );
      case "number":
        return (
          <InputNumber
            min={field.min}
            max={field.max}
            step={field.step}
            style={{ width: "100%" }}
            placeholder={field.placeholder}
          />
        );
      case "color":
        return <ColorPicker />;
      case "upload-audio":
        return (
          <div>
            {uploadedAssets.find((item) => item.type === "audio") ? (
              <div
                style={{
                  padding: "8px 12px",
                  background: "#f6ffed",
                  border: "1px solid #b7eb8f",
                  borderRadius: "6px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}>
                <span style={{ color: "#52c41a" }}>
                  🎵{" "}
                  {
                    uploadedAssets.find((item) => item.type === "audio")
                      ?.filename
                  }
                </span>
                <Button
                  type="text"
                  size="small"
                  icon={<DeleteOutlined />}
                  onClick={() => removeAsset("audio")}
                />
              </div>
            ) : (
              <Upload
                beforeUpload={(file) => handleFileUpload(file, "audio")}
                accept="audio/*"
                showUploadList={false}>
                <Button icon={<UploadOutlined />} style={{ width: "100%" }}>
                  选择本地音频文件
                </Button>
              </Upload>
            )}
          </div>
        );
      case "upload-video":
        return (
          <div>
            {uploadedAssets.find((item) => item.type === "video") ? (
              <div
                style={{
                  padding: "8px 12px",
                  background: "#fff7e6",
                  border: "1px solid #ffd591",
                  borderRadius: "6px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}>
                <span style={{ color: "#fa8c16" }}>
                  🎬{" "}
                  {
                    uploadedAssets.find((item) => item.type === "video")
                      ?.filename
                  }
                </span>
                <Button
                  type="text"
                  size="small"
                  icon={<DeleteOutlined />}
                  onClick={() => removeAsset("video")}
                />
              </div>
            ) : (
              <Upload
                beforeUpload={(file) => handleFileUpload(file, "video")}
                accept="video/*"
                showUploadList={false}>
                <Button icon={<UploadOutlined />} style={{ width: "100%" }}>
                  选择本地视频文件
                </Button>
              </Upload>
            )}
          </div>
        );
      default:
        return <Input placeholder={field.placeholder} />;
    }
  };

  const getCurrentStepConfig = () => stepConfigs[currentStep];

  const renderStepContent = () => {
    if (currentStep >= stepConfigs.length) {
      // 最后一步：项目总览
      return (
        <div>
          <Title level={4} style={{ textAlign: "center", marginBottom: 24 }}>
            <Sparkles size={20} style={{ marginRight: 8 }} />
            项目配置总览
          </Title>

          <Alert
            message="配置完成"
            description="请确认您的项目配置，然后点击生成按钮创建项目"
            type="success"
            showIcon
            style={{ marginBottom: 24 }}
          />

          <Row gutter={16}>
            <Col span={12}>
              <Card title="已启用组件" size="small">
                <Space direction="vertical" style={{ width: "100%" }}>
                  {Object.entries(projectData).map(([key, section]) => {
                    const config = stepConfigs.find((s) => s.key === key);
                    return section.enabled ? (
                      <div
                        key={key}
                        style={{ display: "flex", alignItems: "center" }}>
                        <span style={{ color: config?.color, marginRight: 8 }}>
                          {config?.icon}
                        </span>
                        <Text strong>{config?.title}</Text>
                        <CheckOutlined
                          style={{ color: "#52c41a", marginLeft: 8 }}
                        />
                      </div>
                    ) : null;
                  })}
                  {Object.values(projectData).every(
                    (section) => !section.enabled
                  ) && <Text type="secondary">未启用任何组件</Text>}
                </Space>
              </Card>
            </Col>

            <Col span={12}>
              <Card title="上传素材" size="small">
                <Space direction="vertical" style={{ width: "100%" }}>
                  {uploadedAssets.map((asset, index) => (
                    <div
                      key={index}
                      style={{ display: "flex", alignItems: "center" }}>
                      <span style={{ marginRight: 8 }}>
                        {asset.type === "audio" ? "🎵" : "🎬"}
                      </span>
                      <Text style={{ flex: 1 }}>
                        {asset.filename.length > 20
                          ? asset.filename.substring(0, 17) + "..."
                          : asset.filename}
                      </Text>
                      <CheckOutlined style={{ color: "#52c41a" }} />
                    </div>
                  ))}
                  {uploadedAssets.length === 0 && (
                    <Text type="secondary">未上传任何素材</Text>
                  )}
                </Space>
              </Card>
            </Col>
          </Row>

          <Divider />

          <div style={{ textAlign: "center" }}>
            <Button
              type="primary"
              size="large"
              icon={<Sparkles size={20} />}
              loading={generateMutation.isPending}
              onClick={handleGenerate}
              style={{
                height: 48,
                fontSize: 16,
                paddingLeft: 32,
                paddingRight: 32,
              }}>
              {generateMutation.isPending ? "生成中..." : "生成集成项目"}
            </Button>
            <div style={{ marginTop: 8 }}>
              <Text type="secondary">
                {Object.values(projectData).filter((s) => s.enabled).length ===
                0
                  ? "请返回启用至少一个组件"
                  : `将生成包含 ${
                      Object.values(projectData).filter((s) => s.enabled).length
                    } 个组件的项目`}
              </Text>
            </div>
          </div>
        </div>
      );
    }

    const stepConfig = getCurrentStepConfig();
    const sectionKey = stepConfig.key as keyof ProjectData;
    const isEnabled = projectData[sectionKey].enabled;

    return (
      <div>
        <div style={{ textAlign: "center", marginBottom: 24 }}>
          <div
            style={{ color: stepConfig.color, fontSize: 48, marginBottom: 16 }}>
            {stepConfig.icon}
          </div>
          <Title level={3}>{stepConfig.title}</Title>
          <Text type="secondary">{stepConfig.description}</Text>
        </div>

        <div style={{ marginBottom: 24 }}>
          <Checkbox
            checked={isEnabled}
            onChange={(e) => handleSectionToggle(sectionKey, e.target.checked)}
            style={{ fontSize: 16 }}>
            <Text strong>启用 {stepConfig.title}</Text>
          </Checkbox>
        </div>

        {isEnabled && (
          <div>
            <Divider />
            <Row gutter={[16, 16]}>
              {stepConfig.fields.map((field) => (
                <Col xs={24} sm={12} key={field.name}>
                  <Form.Item
                    name={[stepConfig.key, field.name]}
                    label={field.label}
                    initialValue={field.default}
                    rules={
                      field.required
                        ? [{ required: true, message: `请输入${field.label}` }]
                        : []
                    }>
                    {renderField(field)}
                  </Form.Item>
                </Col>
              ))}
            </Row>
          </div>
        )}
      </div>
    );
  };

  const nextStep = () => {
    if (currentStep < stepConfigs.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleConfigModalClose = () => {
    setConfigModalVisible(false);
    setCurrentStep(0);
    form.resetFields();
    setProjectData({
      text: { enabled: false, config: {} },
      audio: { enabled: false, config: {} },
      video: { enabled: false, config: {} },
      animation: { enabled: false, config: {} },
      effects: { enabled: false, config: {} },
      transition: { enabled: false, config: {} },
    });
  };

  return (
    <div className="create-project">
      <div style={{ marginBottom: "24px" }}>
        <Title level={2}>
          <Space>
            <Film size={32} color="#1890ff" />
            开始创作
          </Space>
        </Title>
        <Paragraph type="secondary">
          点击下方按钮，通过步骤式配置创建您的剪映项目。支持文本、音频、视频、动画、特效等多种元素组合。
        </Paragraph>
      </div>

      <div style={{ textAlign: "center", padding: "80px 0" }}>
        <div style={{ marginBottom: 32 }}>
          <Settings size={64} color="#1890ff" style={{ marginBottom: 16 }} />
          <Title level={3} style={{ margin: 0 }}>
            创建新项目
          </Title>
          <Text type="secondary" style={{ fontSize: 16 }}>
            通过简单的步骤配置，快速生成专业的剪映项目
          </Text>
        </div>

        <Button
          type="primary"
          size="large"
          icon={<PlusOutlined />}
          onClick={() => setConfigModalVisible(true)}
          style={{
            height: 56,
            fontSize: 18,
            paddingLeft: 40,
            paddingRight: 40,
            borderRadius: 8,
          }}>
          开始配置项目
        </Button>
      </div>

      {/* 项目配置弹窗 */}
      <Modal
        title={
          <div style={{ textAlign: "center" }}>
            <Space>
              <Settings size={20} />
              项目配置向导
            </Space>
          </div>
        }
        open={configModalVisible}
        onCancel={handleConfigModalClose}
        width={800}
        footer={null}
        destroyOnHidden>
        
        <div style={{ marginBottom: 24 }}>
          <Steps
            current={currentStep}
            size="small"
            items={[
              ...stepConfigs.map((config, index) => ({
                title: config.title,
                icon: currentStep === index ? config.icon : undefined,
                status: (currentStep === index
                  ? "process"
                  : currentStep > index
                  ? "finish"
                  : "wait") as "process" | "finish" | "wait",
              })),
              {
                title: "生成项目",
                icon:
                  currentStep === stepConfigs.length ? (
                    <Sparkles size={16} />
                  ) : undefined,
                status: (currentStep === stepConfigs.length
                  ? "process"
                  : currentStep > stepConfigs.length
                  ? "finish"
                  : "wait") as "process" | "finish" | "wait",
              },
            ]}
          />
        </div>

        <div style={{ minHeight: 400, padding: "24px 0" }}>
          <Form form={form} layout="vertical">
            {renderStepContent()}
          </Form>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            paddingTop: 16,
            borderTop: "1px solid #f0f0f0",
          }}>
          <Button
            icon={<ArrowLeftOutlined />}
            onClick={prevStep}
            disabled={currentStep === 0}>
            上一步
          </Button>

          <div>
            <Text type="secondary" style={{ marginRight: 16 }}>
              {currentStep + 1} / {stepConfigs.length + 1}
            </Text>

            {currentStep < stepConfigs.length ? (
              <Button
                type="primary"
                icon={<ArrowRightOutlined />}
                onClick={nextStep}>
                下一步
              </Button>
            ) : null}
          </div>
        </div>
      </Modal>

      {/* 结果预览模态框 */}
      <Modal
        title="🎉 项目生成完成"
        open={previewVisible}
        onCancel={() => {
          setPreviewVisible(false);
          setGeneratedResult(null);
        }}
        footer={[
          <Button
            key="close"
            onClick={() => {
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
                navigator.clipboard.writeText(
                  JSON.stringify(generatedResult, null, 2)
                );
                message.success("已复制到剪贴板");
              }
            }}>
            复制结果
          </Button>,
          <Button
            key="download-json"
            onClick={() => {
              if (generatedResult) {
                const blob = new Blob(
                  [JSON.stringify(generatedResult.data, null, 2)],
                  {
                    type: "application/json",
                  }
                );
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `draft_content_${Date.now()}.json`;
                a.click();
                URL.revokeObjectURL(url);
                message.success("JSON文件下载完成");
              }
            }}>
            下载JSON
          </Button>,
        ]}
        width={900}
        destroyOnHidden>
        {generatedResult ? (
          <div>
            <Alert
              message={generatedResult.message || "项目生成成功"}
              description={
                <div>
                  <div>
                    项目总时长:{" "}
                    {generatedResult.summary?.total_duration || "未知"}
                  </div>
                  <div>
                    包含组件: {generatedResult.summary?.components_count || 0}{" "}
                    个
                  </div>
                  <div>
                    启用功能:{" "}
                    {generatedResult.summary?.enabled_features?.join(", ") ||
                      "无"}
                  </div>
                </div>
              }
              type="success"
              showIcon
              style={{ marginBottom: 16 }}
            />

            <Tabs
              items={[
                {
                  key: "json",
                  label: "完整JSON",
                  children: (
                    <div style={{ height: "400px" }}>
                      <Editor
                        height="100%"
                        defaultLanguage="json"
                        value={JSON.stringify(
                          generatedResult.data || generatedResult,
                          null,
                          2
                        )}
                        options={{
                          readOnly: true,
                          minimap: { enabled: false },
                          fontSize: 12,
                          theme: "vs-light",
                          wordWrap: "on",
                        }}
                      />
                    </div>
                  ),
                },
                {
                  key: "summary",
                  label: "组件摘要",
                  children: (
                    <div style={{ height: "400px", overflow: "auto" }}>
                      {generatedResult.summary?.segments?.length > 0 ? (
                        <List
                          size="small"
                          dataSource={generatedResult.summary.segments}
                          renderItem={(item: any) => (
                            <List.Item>
                              <List.Item.Meta
                                title={`${item.type} - ${
                                  item.start_time || "时间未知"
                                }`}
                                description={
                                  <div>
                                    {item.content && (
                                      <div>内容: {item.content}</div>
                                    )}
                                    {item.duration && (
                                      <div>时长: {item.duration}</div>
                                    )}
                                    {item.file_exists !== undefined && (
                                      <div
                                        style={{
                                          color: item.file_exists
                                            ? "#52c41a"
                                            : "#faad14",
                                        }}>
                                        素材状态:{" "}
                                        {item.file_exists
                                          ? "✅ 文件存在"
                                          : "⚠️ 需要素材文件"}
                                      </div>
                                    )}
                                    {item.note && (
                                      <div style={{ color: "#faad14" }}>
                                        注意: {item.note}
                                      </div>
                                    )}
                                  </div>
                                }
                              />
                            </List.Item>
                          )}
                        />
                      ) : (
                        <div style={{ textAlign: "center", padding: "20px" }}>
                          <Text type="secondary">暂无组件信息</Text>
                        </div>
                      )}
                    </div>
                  ),
                },
                {
                  key: "assets",
                  label: "素材文件",
                  children: (
                    <div style={{ height: "400px", overflow: "auto" }}>
                      {uploadedAssets.length > 0 ||
                      generatedResult.summary?.assets?.length > 0 ? (
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
                              <Text strong style={{ color: "#1890ff" }}>
                                用户素材:
                              </Text>
                              <List
                                size="small"
                                dataSource={uploadedAssets}
                                renderItem={(asset: UploadedAsset) => (
                                  <List.Item>
                                    <List.Item.Meta
                                      title={
                                        <Space>
                                          <span>{asset.filename}</span>
                                          <span
                                            style={{
                                              fontSize: "12px",
                                              padding: "2px 6px",
                                              borderRadius: "4px",
                                              backgroundColor:
                                                asset.type === "video"
                                                  ? "#1890ff"
                                                  : "#52c41a",
                                              color: "white",
                                            }}>
                                            {asset.type}
                                          </span>
                                          <span
                                            style={{
                                              fontSize: "12px",
                                              padding: "2px 6px",
                                              borderRadius: "4px",
                                              backgroundColor: "#52c41a",
                                              color: "white",
                                            }}>
                                            本地
                                          </span>
                                        </Space>
                                      }
                                      description={
                                        <div>
                                          {asset.size && (
                                            <div>
                                              文件大小:{" "}
                                              {(
                                                asset.size /
                                                (1024 * 1024)
                                              ).toFixed(2)}{" "}
                                              MB
                                            </div>
                                          )}
                                          <div
                                            style={{
                                              fontSize: "12px",
                                              color: "#666",
                                              marginTop: "4px",
                                            }}>
                                            来源: 用户上传的
                                            {asset.type === "audio"
                                              ? "音频"
                                              : "视频"}
                                            文件
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
                              <Text strong style={{ color: "#666" }}>
                                系统默认素材:
                              </Text>
                              <List
                                size="small"
                                dataSource={generatedResult.summary.assets}
                                renderItem={(asset: any) => (
                                  <List.Item>
                                    <List.Item.Meta
                                      title={
                                        <Space>
                                          <span>{asset.filename}</span>
                                          <span
                                            style={{
                                              fontSize: "12px",
                                              padding: "2px 6px",
                                              borderRadius: "4px",
                                              backgroundColor: "#666",
                                              color: "white",
                                            }}>
                                            {asset.type}
                                          </span>
                                        </Space>
                                      }
                                      description={
                                        <div>
                                          <div>{asset.description}</div>
                                          <div
                                            style={{
                                              fontSize: "12px",
                                              color: "#666",
                                              marginTop: "4px",
                                            }}>
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

                          <div style={{ marginTop: 16, textAlign: "center" }}>
                            <Button
                              type="primary"
                              onClick={handleDownloadPatch}>
                              📦 下载完整补丁包
                            </Button>
                          </div>
                        </div>
                      ) : (
                        <div style={{ textAlign: "center", padding: "20px" }}>
                          <Text type="secondary">当前项目无需素材文件</Text>
                          <br />
                          <Text type="secondary" style={{ fontSize: "12px" }}>
                            请在相应组件中上传音视频文件，或启用需要素材的组件
                          </Text>
                        </div>
                      )}
                    </div>
                  ),
                },
              ]}
            />
          </div>
        ) : (
          <div style={{ textAlign: "center", padding: "20px" }}>
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
        loading={createLoading}
      />
    </div>
  );
};

export default CreateProject;
