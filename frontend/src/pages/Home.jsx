import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, Card, Row, Col, Typography, Space } from 'antd';
import { SearchOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const hotGanzhi = [
  '甲子', '乙丑', '丙寅', '丁卯', '戊辰',
  '己巳', '庚午', '辛未', '壬申', '癸酉'
];

const Home = () => {
  const navigate = useNavigate();
  const [searchValue, setSearchValue] = useState('');

  const handleSearch = (value) => {
    if (value) {
      navigate(`/ganzhi/${value}`);
    }
  };

  const quickEntries = [
    { key: 'nayin', label: '纳音专题', desc: '纳音五行分类查询' },
    { key: 'shensha', label: '神煞字典', desc: '神煞知识详解' },
    { key: 'guanxi', label: '关系图谱', desc: '干支关系可视化' },
    { key: 'compare', label: '干支对比', desc: '多柱对比分析' },
  ];

  return (
    <div style={{ padding: '24px', maxWidth: 1200, margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: 48 }}>
        <Title level={1}>六十甲子象意百科</Title>
        <Text type="secondary">探索中国传统文化的智慧宝库</Text>
      </div>

      <div style={{ marginBottom: 48 }}>
        <Input.Search
          size="large"
          placeholder="输入干支名称搜索（如：甲子）"
          prefix={<SearchOutlined />}
          enterButton="搜索"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          onSearch={handleSearch}
          style={{ maxWidth: 600 }}
        />
      </div>

      <div style={{ marginBottom: 48 }}>
        <Title level={4}>热门干支</Title>
        <Row gutter={[16, 16]}>
          {hotGanzhi.map((gz) => (
            <Col xs={12} sm={8} md={4} key={gz}>
              <Card
                hoverable
                onClick={() => navigate(`/ganzhi/${gz}`)}
                style={{ textAlign: 'center' }}
              >
                {gz}
              </Card>
            </Col>
          ))}
        </Row>
      </div>

      <div>
        <Title level={4}>快速入口</Title>
        <Row gutter={[16, 16]}>
          {quickEntries.map((entry) => (
            <Col xs={12} sm={6} key={entry.key}>
              <Card
                hoverable
                onClick={() => navigate(`/${entry.key}`)}
                style={{ textAlign: 'center' }}
              >
                <Space direction="vertical" size={0}>
                  <Text strong>{entry.label}</Text>
                  <Text type="secondary">{entry.desc}</Text>
                </Space>
              </Card>
            </Col>
          ))}
        </Row>
      </div>
    </div>
  );
};

export default Home;
