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

export interface User {
  id: number;
  username: string;
  email?: string;
  nickname?: string;
  phone?: string;
  avatar?: string;
  is_active: boolean;
  is_admin?: boolean;
  last_login?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateUserData {
  username: string;
  email?: string;
  nickname?: string;
  is_active?: boolean;
}

export interface UpdateUserData {
  username?: string;
  email?: string;
  nickname?: string;
  is_active?: boolean;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  password: string;
  confirmPassword?: string;
  email?: string;
  nickname?: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data?: {
    user: User;
    token: string;
  };
}

class ApiService {
  private token: string | null = null;

  constructor() {
    // 从localStorage获取token
    this.token = localStorage.getItem('auth_token');
    this.setupInterceptors();
  }

  private setupInterceptors() {
    // 请求拦截器 - 添加认证头
    axios.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });

    // 响应拦截器 - 处理认证错误
    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.logout();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // 认证相关 - 使用箭头函数保持this上下文
  login = async (loginData: LoginData): Promise<AuthResponse> => {
    console.log('发送登录请求，数据:', loginData);
    const { data } = await axios.post(`${API_BASE_URL}/auth/login`, loginData);
    console.log('登录响应:', data);
    if (data.success && data.data?.token) {
      this.setToken(data.data.token);
    }
    return data;
  }
  
  register = async (registerData: RegisterData): Promise<AuthResponse> => {
    console.log('发送注册请求，数据:', registerData);
    const { data } = await axios.post(`${API_BASE_URL}/auth/register`, registerData);
    console.log('注册响应:', data);
    if (data.success && data.data?.token) {
      this.setToken(data.data.token);
    }
    return data;
  }

  async logout(): Promise<void> {
    try {
      await axios.post(`${API_BASE_URL}/auth/logout`);
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.clearToken();
    }
  }

  async getCurrentUser(): Promise<User> {
    const { data } = await axios.get(`${API_BASE_URL}/auth/me`);
    return data.data;
  }

  async updateProfile(profileData: UpdateUserData): Promise<User> {
    const { data } = await axios.put(`${API_BASE_URL}/auth/profile`, profileData);
    return data.data;
  }

  async changePassword(passwordData: { old_password: string; new_password: string }) {
    const { data } = await axios.post(`${API_BASE_URL}/auth/change-password`, passwordData);
    return data;
  }

  // Token管理
  setToken(token: string) {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  getToken(): string | null {
    return this.token;
  }

  isAuthenticated(): boolean {
    return !!this.token;
  }

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

  // 项目管理相关
  async getProjects() {
    const { data } = await axios.get(`${API_BASE_URL}/projects`);
    return data;
  }

  async getProject(projectId: number) {
    const { data } = await axios.get(`${API_BASE_URL}/projects/${projectId}`);
    return data;
  }

  async updateProject(projectId: number, projectData: any) {
    const { data } = await axios.put(`${API_BASE_URL}/projects/${projectId}`, projectData);
    return data;
  }

  async deleteProject(projectId: number) {
    const { data } = await axios.delete(`${API_BASE_URL}/projects/${projectId}`);
    return data;
  }

  // 仪表盘数据
  async getDashboardData() {
    const { data } = await axios.get(`${API_BASE_URL}/dashboard`);
    return data;
  }

  // 统计信息
  async getProjectStats() {
    const { data } = await axios.get(`${API_BASE_URL}/stats`);
    return data;
  }

  // 用户管理相关
  async getUsers() {
    const { data } = await axios.get(`${API_BASE_URL}/users`);
    return data;
  }

  async getUser(userId: number) {
    const { data } = await axios.get(`${API_BASE_URL}/users/${userId}`);
    return data;
  }

  async createUser(userData: CreateUserData) {
    const { data } = await axios.post(`${API_BASE_URL}/users`, userData);
    return data;
  }

  async updateUser(userId: number, userData: UpdateUserData) {
    const { data } = await axios.put(`${API_BASE_URL}/users/${userId}`, userData);
    return data;
  }

  async deleteUser(userId: number) {
    const { data } = await axios.delete(`${API_BASE_URL}/users/${userId}`);
    return data;
  }
}

export const apiService = new ApiService();
