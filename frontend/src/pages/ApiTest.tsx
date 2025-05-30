import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Result, Button } from 'antd';

const ApiTest: React.FC = () => {
  const navigate = useNavigate();
  
  // 自动重定向到主页
  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/');
    }, 2000);
    
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <Result
      status="404"
      title="页面已移除"
      subTitle="API 测试功能已经被移除，请使用其他功能。"
      extra={
        <Button type="primary" onClick={() => navigate('/')}>
          返回首页
        </Button>
      }
    />
  );
};

export default ApiTest;
