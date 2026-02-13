import { useState } from 'react';
import { Card, Form, Input, Button, Tabs, Table, Typography, message, Upload, Modal } from 'antd';
import { UploadOutlined, DownloadOutlined, LoginOutlined } from '@ant-design/icons';
import * as api from '../services/api';

const { Title, Text } = Typography;
const { TabPane } = Tabs;

const Admin = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('ganzhi');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleLogin = async (values) => {
    try {
      setLoginLoading(true);
      await api.adminLogin(values);
      setIsLoggedIn(true);
      message.success('登录成功');
    } catch (error) {
      message.error('登录失败');
    } finally {
      setLoginLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await api.adminExport();
      const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'liushijiazi_export.json';
      a.click();
      URL.revokeObjectURL(url);
      message.success('导出成功');
    } catch (error) {
      message.error('导出失败');
    }
  };

  const handleImport = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const json = JSON.parse(e.target.result);
        message.success('文件解析成功，请提交');
      } catch (error) {
        message.error('文件格式错误');
      }
    };
    reader.readAsText(file);
    return false;
  };

  const columns = {
    ganzhi: [
      { title: 'ID', dataIndex: 'id', key: 'id' },
      { title: '干支', dataIndex: 'ganzhi', key: 'ganzhi' },
      { title: '天干', dataIndex: 'tiangan', key: 'tiangan' },
      { title: '地支', dataIndex: 'dizhi', key: 'dizhi' },
      { title: '天干五行', dataIndex: 'tiangan_wuxing', key: 'tiangan_wuxing' },
    ],
    nayin: [
      { title: 'ID', dataIndex: 'id', key: 'id' },
      { title: '干支', dataIndex: 'ganzhi', key: 'ganzhi' },
      { title: '纳音', dataIndex: 'nayin_name', key: 'nayin_name' },
      { title: '纳音五行', dataIndex: 'nayin_wuxing', key: 'nayin_wuxing' },
      { title: '状态', dataIndex: 'zhuangtai', key: 'zhuangtai' },
    ],
    xiangyi: [
      { title: 'ID', dataIndex: 'id', key: 'id' },
      { title: '干支ID', dataIndex: 'ganzhi_id', key: 'ganzhi_id' },
      { title: '类型', dataIndex: 'type', key: 'type' },
      { title: '类别', dataIndex: 'category', key: 'category' },
      { title: '象意', dataIndex: 'content', key: 'content' },
    ],
    shensha: [
      { title: 'ID', dataIndex: 'id', key: 'id' },
      { title: '名称', dataIndex: 'name', key: 'name' },
      { title: '类型', dataIndex: 'type', key: 'type' },
      { title: '吉凶', dataIndex: 'jixiong', key: 'jixiong' },
    ],
  };

  if (!isLoggedIn) {
    return (
      <div style={{ padding: 24, maxWidth: 400, margin: '0 auto' }}>
        <Card>
          <Title level={3} style={{ textAlign: 'center' }}>管理员登录</Title>
          <Form layout="vertical" onFinish={handleLogin}>
            <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
              <Input placeholder="请输入用户名" />
            </Form.Item>
            <Form.Item name="password" label="密码" rules={[{ required: true }]}>
              <Input.Password placeholder="请输入密码" />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" block loading={loginLoading}>
                <LoginOutlined /> 登录
              </Button>
            </Form.Item>
          </Form>
          <Text type="secondary" style={{ display: 'block', textAlign: 'center' }}>
            Phase 1: 使用预设账户 admin/admin123
          </Text>
        </Card>
      </div>
    );
  }

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <Title level={2}>管理后台</Title>

      <Card style={{ marginBottom: 24 }}>
        <Row gutter={[16, 16]}>
          <Col>
            <Upload beforeUpload={handleImport} showUploadList={false}>
              <Button icon={<UploadOutlined />}>导入数据</Button>
            </Upload>
          </Col>
          <Col>
            <Button icon={<DownloadOutlined />} onClick={handleExport}>
              导出数据
            </Button>
          </Col>
        </Row>
      </Card>

      <Card>
        <Tabs activeKey={activeTab} onChange={setActiveTab}>
          <TabPane tab="干支管理" key="ganzhi">
            <Table
              columns={columns.ganzhi}
              dataSource={data}
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          </TabPane>
          <TabPane tab="纳音管理" key="nayin">
            <Table
              columns={columns.nayin}
              dataSource={data}
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          </TabPane>
          <TabPane tab="象意管理" key="xiangyi">
            <Table
              columns={columns.xiangyi}
              dataSource={data}
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          </TabPane>
          <TabPane tab="神煞管理" key="shensha">
            <Table
              columns={columns.shensha}
              dataSource={data}
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

export default Admin;
