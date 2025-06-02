// API服务层
const API_BASE_URL = 'http://localhost:5000';

interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  // 添加健康检查特有的字段
  version?: string;
  status?: string;
}

interface HealthCheckResponse extends ApiResponse {
  version: string;
  status: string;
}

class ApiService {
  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<HealthCheckResponse> {
    return this.request('/api/health');
  }

  async createBasicProject(): Promise<ApiResponse> {
    return this.request('/api/basic-project', {
      method: 'POST',
    });
  }

  async createTextSegment(data: {
    text?: string;
    duration?: string;
    font?: string;
    color?: number[];
  }): Promise<ApiResponse> {
    return this.request('/api/text-segment', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async createComprehensive(): Promise<ApiResponse> {
    return this.request('/api/comprehensive', {
      method: 'POST',
    });
  }

  async createComprehensiveProject(config: any): Promise<ApiResponse> {
    return this.request('/api/comprehensive-create', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  async downloadFromUrl(data: {
    url: string;
    type: 'audio' | 'video';
  }): Promise<ApiResponse> {
    return this.request('/api/download-from-url', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async selectProjectDir(data: {
    project_data: any;
    project_dir: string;
  }): Promise<ApiResponse> {
    return this.request('/api/select-project-dir', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async downloadPatchSimple(data: {
    project_data: any;
    project_dir: string;
  }): Promise<ApiResponse> {
    return this.request('/api/download-patch-simple', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const apiService = new ApiService();
