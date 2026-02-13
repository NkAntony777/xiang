import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Tabs, Table, Typography, Spin, message, Row, Col } from 'antd';
import * as api from '../services/api';

const { Title, Text } = Typography;
const { TabPane } = Tabs;

const GanzhiDetail = () => {
  const { ganzhi } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    loadGanzhiDetail();
  }, [ganzhi]);

  const loadGanzhiDetail = async () => {
    try {
      setLoading(true);
      const response = await api.getGanzhiDetail(ganzhi);
      setData(response.data);
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

  if (!data) {
    return (
      <div style={{ textAlign: 'center', padding: 48 }}>
        <Text>未找到相关数据</Text>
      </div>
    );
  }

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <Card>
        <Title level={2} style={{ textAlign: 'center' }}>{ganzhi}</Title>

        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col xs={12} md={6}>
            <Text type="secondary">天干:</Text> {data.tiangan} ({data.tiangan_wuxing}, {data.yinyang})
          </Col>
          <Col xs={12} md={6}>
            <Text type="secondary">地支:</Text> {data.dizhi} ({data.dizhi_wuxing})
          </Col>
          <Col xs={12} md={6}>
            <Text type="secondary">方位:</Text> {data.fangwei}
          </Col>
          <Col xs={12} md={6}>
            <Text type="secondary">季节:</Text> {data.jijie}
          </Col>
        </Row>

        {data.nayin && (
          <div style={{ marginBottom: 24 }}>
            <Title level={4}>纳音</Title>
            <Card size="small">
              <Row gutter={[16, 8]}>
                <Col xs={12} md={6}><Text type="secondary">纳音名称:</Text> {data.nayin.nayin_name}</Col>
                <Col xs={12} md={6}><Text type="secondary">纳音五行:</Text> {data.nayin.nayin_wuxing}</Col>
                <Col xs={12} md={6}><Text type="secondary">长生状态:</Text> {data.nayin.zhuangtai}</Col>
                <Col xs={12} md={6}><Text type="secondary">盛大/小弱:</Text> {data.nayin.shengda_xiaoruo}</Col>
              </Row>
            </Card>
          </div>
        )}

        <Tabs defaultActiveKey="1">
          <TabPane tab="象意" key="1">
            <Table
              dataSource={data.xiangyi || []}
              rowKey="id"
              pagination={false}
              columns={[
                { title: '类型', dataIndex: 'type', key: 'type' },
                { title: '类别', dataIndex: 'category', key: 'category' },
                { title: '象意', dataIndex: 'content', key: 'content' },
                { title: '描述', dataIndex: 'description', key: 'description' },
              ]}
            />
          </TabPane>
          <TabPane tab="神煞" key="2">
            <Table
              dataSource={data.shensha || []}
              rowKey="id"
              pagination={false}
              columns={[
                { title: '神煞名称', dataIndex: 'name', key: 'name' },
                { title: '吉凶', dataIndex: 'jixiong', key: 'jixiong' },
                { title: '查法', dataIndex: 'check_method', key: 'check_method' },
                { title: '现代解读', dataIndex: 'modern_desc', key: 'modern_desc' },
              ]}
            />
          </TabPane>
          <TabPane tab="喜忌" key="3">
            <Table
              dataSource={data.xiji || []}
              rowKey="id"
              pagination={false}
              columns={[
                { title: '类型', dataIndex: 'type', key: 'type' },
                { title: '对象类型', dataIndex: 'target_type', key: 'target_type' },
                { title: '对象值', dataIndex: 'target_value', key: 'target_value' },
                { title: '备注', dataIndex: 'remark', key: 'remark' },
              ]}
            />
          </TabPane>
          <TabPane tab="关系" key="4">
            <Table
              dataSource={data.guanxi || []}
              rowKey="id"
              pagination={false}
              columns={[
                { title: '关系干支', dataIndex: 'ganzhi2', key: 'ganzhi2', render: (text) => (
                  <a onClick={() => navigate(`/ganzhi/${text}`)}>{text}</a>
                )},
                { title: '关系类型', dataIndex: 'relation_type', key: 'relation_type' },
                { title: '备注', dataIndex: 'remark', key: 'remark' },
              ]}
            />
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

export default GanzhiDetail;
