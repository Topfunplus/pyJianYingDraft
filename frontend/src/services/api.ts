import axios, { AxiosResponse } from 'axios';

const api = axios.create({
    // @ts-ignore
    baseURL: import.meta.env.DEV ? '/api' : '/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 请求拦截器
api.interceptors.request.use(
    (config) => {
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('❌ Request Error:', error);
        return Promise.reject(error);
    }
);

// 响应拦截器
api.interceptors.response.use(
    (response: AxiosResponse) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`);
        return response;
    },
    (error) => {
        console.error('❌ Response Error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

export interface ApiResponse<T = any> {
    success: boolean;
    message: string;
    data?: T;
    error?: string;
    note?: string;
    animation?: string;
    transition?: string;
    fill_type?: string;
    intensity?: number;
}

export interface HealthCheckResponse {
    success: boolean;
    message: string;
    endpoints: Record<string, string>;
    version: string;
    status: string;
}

export interface ProjectConfig {
    text?: string;
    duration?: string;
    color?: number[];
    font?: string;
    volume?: number;
    fade_in?: string;
    animation_type?: string;
    transition_type?: string;
    fill_type?: string;
    intensity?: number;
    effect_type?: string;
}

export const apiService = {
  // 健康检查
  healthCheck: (): Promise<HealthCheckResponse> =>
    api.get('/health').then(res => res.data),

  // 基础项目
  createBasicProject: (): Promise<ApiResponse> =>
    api.post('/basic-project').then(res => res.data),

  // 文本片段
  createTextSegment: (config: ProjectConfig): Promise<ApiResponse> =>
    api.post('/text-segment', config).then(res => res.data),

  // 音频片段
  createAudioSegment: (config: ProjectConfig): Promise<ApiResponse> =>
    api.post('/audio-segment', config).then(res => res.data),

  // 视频片段
  createVideoSegment: (config: ProjectConfig): Promise<ApiResponse> =>
    api.post('/video-segment', config).then(res => res.data),

  // 视频动画
  createVideoAnimation: (config: ProjectConfig): Promise<ApiResponse> =>
    api.post('/video-animation', config).then(res => res.data),

  // 文本动画
  createTextAnimation: (config: ProjectConfig): Promise<ApiResponse> =>
    api.post('/text-animation', config).then(res => res.data),

  // 转场效果
  createTransition: (config: ProjectConfig): Promise<ApiResponse> =>
    api.post('/transition', config).then(res => res.data),

  // 背景填充
  createBackgroundFilling: (config: ProjectConfig): Promise<ApiResponse> =>
    api.post('/background-filling', config).then(res => res.data),

  // 文本特效
  createTextEffects: (config: ProjectConfig): Promise<ApiResponse> =>
    api.post('/text-effects', config).then(res => res.data),

  // 综合项目（原版本）
  createComprehensive: (): Promise<ApiResponse> =>
    api.post('/comprehensive').then(res => res.data),

  // 综合创作项目（新的集成版本）
  createComprehensiveProject: (config: any): Promise<ApiResponse> =>
    api.post('/comprehensive-create', config).then(res => res.data),
};

export default api;
