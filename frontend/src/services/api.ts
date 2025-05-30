import axios from 'axios';

// API基础URL
const API_BASE_URL = '/api';

export interface ProjectConfig {
  text?: string;
  duration?: string;
  volume?: number;
  color?: [number, number, number];
  fade_in?: string;
  animation_type?: string;
  font?: string;
  [key: string]: any;
}

class ApiService {
  // 健康检查
  async healthCheck() {
    const { data } = await axios.get(`${API_BASE_URL}/health`);
    return data;
  }

  // 创建基础项目
  async createBasicProject() {
    const { data } = await axios.post(`${API_BASE_URL}/basic-project`);
    return data;
  }

  // 创建文本片段
  async createTextSegment(config: ProjectConfig = {}) {
    const { data } = await axios.post(`${API_BASE_URL}/text-segment`, config);
    return data;
  }

  // 创建综合项目
  async createComprehensive() {
    const { data } = await axios.post(`${API_BASE_URL}/comprehensive`);
    return data;
  }

  // 创建综合定制项目
  async createComprehensiveProject(config: any) {
    const { data } = await axios.post(`${API_BASE_URL}/comprehensive-create`, config);
    return data;
  }
}

export const apiService = new ApiService();
