import React from "react";
import { Space, Typography} from "antd";

import { Film } from "lucide-react";

const { Title } = Typography;

const Dashboard: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: "24px" }}>
        <Title level={2}>
          <Space>
            <Film size={32} color="#1890ff" />
            仪表盘
          </Space>
        </Title>
      </div>
    </div>
  );
};

export default Dashboard;
