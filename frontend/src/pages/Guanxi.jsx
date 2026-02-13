import { useState, useEffect, useRef } from 'react';
import { Card, Typography, Spin, message, Select, Row, Col } from 'antd';
import * as echarts from 'echarts';
import * as api from '../services/api';

const { Title, Text } = Typography;
const { Option } = Select;

const Guanxi = () => {
  const chartRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [guanxiData, setGuanxiData] = useState({ nodes: [], links: [] });
  const [relationTypes, setRelationTypes] = useState([]);
  const [selectedType, setSelectedType] = useState(null);

  useEffect(() => {
    loadGuanxiData();
    loadRelationTypes();
  }, []);

  useEffect(() => {
    if (guanxiData.nodes.length) {
      renderChart();
    }
  }, [guanxiData, selectedType]);

  const loadGuanxiData = async () => {
    try {
      setLoading(true);
      const response = await api.getAllGuanxi();
      setGuanxiData(response.data);
    } catch (error) {
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  const loadRelationTypes = async () => {
    try {
      const response = await api.getGuanxiTypes();
      setRelationTypes(response.data);
    } catch (error) {
      console.error('加载关系类型失败', error);
    }
  };

  const renderChart = () => {
    if (!chartRef.current) return;

    const chart = echarts.init(chartRef.current);

    // Filter data based on selected type
    let nodes = [...guanxiData.nodes];
    let links = [...(guanxiData.links || [])];

    if (selectedType) {
      links = links.filter((l) => l.relation_type === selectedType);
      const relatedNodes = new Set();
      links.forEach((l) => {
        relatedNodes.add(l.source);
        relatedNodes.add(l.target);
      });
      nodes = nodes.filter((n) => relatedNodes.has(n.name));
    }

    const relationColors = {
      '六合': '#52c41a',
      '三合': '#1890ff',
      '半合': '#13c2c2',
      '六冲': '#f5222d',
      '六害': '#faad14',
      '三刑': '#eb2f96',
      '自刑': '#722ed1',
      '同位': '#fa8c16',
      '隔八生子': '#2f54eb',
    };

    const option = {
      title: {
        text: '干支关系图谱',
        left: 'center',
      },
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          if (params.dataType === 'edge') {
            return `${params.data.source} - ${params.data.relation_type} - ${params.data.target}`;
          }
          return params.name;
        },
      },
      series: [
        {
          type: 'graph',
          layout: 'force',
          roam: true,
          label: {
            show: true,
            position: 'right',
          },
          force: {
            repulsion: 200,
            edgeLength: 100,
          },
          data: nodes.map((n) => ({
            name: n.name,
            symbolSize: 30,
            itemStyle: {
              color: n.category === '天干' ? '#1890ff' : n.category === '地支' ? '#52c41a' : '#722ed1',
            },
          })),
          links: links.map((l) => ({
            source: l.source,
            target: l.target,
            relation_type: l.relation_type,
            lineStyle: {
              color: relationColors[l.relation_type] || '#999',
              width: 2,
              curveness: 0.1,
            },
          })),
          lineStyle: {
            curveness: 0.1,
          },
        },
      ],
    };

    chart.setOption(option);

    window.addEventListener('resize', () => chart.resize());
    return () => chart.dispose();
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 48 }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div style={{ padding: 24, maxWidth: 1400, margin: '0 auto' }}>
      <Title level={2}>干支关系图谱</Title>

      <Card style={{ marginBottom: 24 }}>
        <Row gutter={[16, 16]} align="middle">
          <Col>
            <Text>关系类型筛选：</Text>
          </Col>
          <Col>
            <Select
              placeholder="选择关系类型"
              allowClear
              style={{ width: 150 }}
              value={selectedType}
              onChange={setSelectedType}
            >
              {relationTypes.map((type) => (
                <Option key={type} value={type}>{type}</Option>
              ))}
            </Select>
          </Col>
        </Row>
      </Card>

      <Card>
        <div ref={chartRef} style={{ height: 600, width: '100%' }} />
      </Card>
    </div>
  );
};

export default Guanxi;
