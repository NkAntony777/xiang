import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Row, Col, Typography, Table, Spin, message, Tag, Tabs } from 'antd';
import * as api from '../services/api';

const { Title, Text } = Typography;
const { TabPane } = Tabs;

const Nayin = () => {
  const { status } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [nayinData, setNayinData] = useState([]);
  const [statusList, setStatusList] = useState([]);

  useEffect(() => {
    if (status) {
      loadNayinByStatus(status);
    } else {
      loadNayinStatusList();
    }
  }, [status]);

  const loadNayinStatusList = async () => {
    try {
      setLoading(true);
      const response = await api.getNayinStatusList();
      setStatusList(response.data);
      // Also load all nayin data
      const allNayin = [];
      for (const s of response.data) {
        const res = await api.getNayinByStatus(s);
        allNayin.push(...res.data);
      }
      setNayinData(allNayin);
    } catch (error) {
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  const loadNayinByStatus = async (statusName) => {
    try {
      setLoading(true);
      const response = await api.getNayinByStatus(statusName);
      setNayinData(response.data);
    } catch (error) {
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 48 }}>
        <Spin size="large" />
      </div>
    );
  }

  const columns = [
    {
      title: '干支',
      dataIndex: 'ganzhi',
      key: 'ganzhi',
      render: (text) => <a onClick={() => navigate(`/ganzhi/${text}`)}>{text}</a>,
    },
    { title: '纳音', dataIndex: 'nayin_name', key: 'nayin_name' },
    { title: '纳音五行', dataIndex: 'nayin_wuxing', key: 'nayin_wuxing' },
    {
      title: '状态',
      dataIndex: 'zhuangtai',
      key: 'zhuangtai',
      render: (text) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: '分类',
      dataIndex: 'shengda_xiaoruo',
      key: 'shengda_xiaoruo',
      render: (text) => (
        <Tag color={text === '盛大' ? 'green' : 'orange'}>{text}</Tag>
      ),
    },
  ];

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <Title level={2}>纳音专题</Title>

      <Card style={{ marginBottom: 24 }}>
        <Text type="secondary">十二长生状态</Text>
        <Row gutter={[8, 8]} style={{ marginTop: 8 }}>
          {['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养'].map((s) => (
            <Col key={s}>
              <Tag
                color={status === s ? 'blue' : 'default'}
                style={{ cursor: 'pointer' }}
                onClick={() => navigate(`/nayin/status/${s}`)}
              >
                {s}
              </Tag>
            </Col>
          ))}
        </Row>
      </Card>

      <Card>
        <Tabs defaultActiveKey="1">
          <TabPane tab={status || '全部'} key="1">
            <Table
              columns={columns}
              dataSource={nayinData}
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

export default Nayin;
