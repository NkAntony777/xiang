import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Select, Button, Table, Typography, Space, message } from 'antd';
import { SwapOutlined } from '@ant-design/icons';
import * as api from '../services/api';

const { Title, Text } = Typography;
const { Option } = Select;

const allGanzhi = [
  '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
  '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
  '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
  '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
  '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
  '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
];

const Compare = () => {
  const navigate = useNavigate();
  const [selectedGanzhi, setSelectedGanzhi] = useState([]);
  const [compareData, setCompareData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleCompare = async () => {
    if (selectedGanzhi.length < 2) {
      message.warning('请选择至少2个干支进行对比');
      return;
    }
    try {
      setLoading(true);
      const response = await api.compareGanzhi(selectedGanzhi);
      setCompareData(response.data);
    } catch (error) {
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: '属性',
      dataIndex: 'field',
      key: 'field',
      fixed: 'left',
      width: 120,
    },
    ...selectedGanzhi.map((gz) => ({
      title: gz,
      dataIndex: gz,
      key: gz,
      width: 150,
      render: (text, record) => {
        if (record.field === '操作') {
          return <a onClick={() => navigate(`/ganzhi/${gz}`)}>查看详情</a>;
        }
        return text;
      },
    })),
  ];

  const getTableData = () => {
    if (!compareData.length) return [];
    const fields = ['天干', '地支', '天干五行', '地支五行', '阴阳', '方位', '季节', '纳音', '纳音五行', '长生状态', '操作'];
    return fields.map((field) => {
      const row = { field, key: field };
      selectedGanzhi.forEach((gz) => {
        const item = compareData.find((d) => d.ganzhi === gz);
        switch (field) {
          case '天干': row[gz] = item?.tiangan || '-'; break;
          case '地支': row[gz] = item?.dizhi || '-'; break;
          case '天干五行': row[gz] = item?.tiangan_wuxing || '-'; break;
          case '地支五行': row[gz] = item?.dizhi_wuxing || '-'; break;
          case '阴阳': row[gz] = item?.yinyang || '-'; break;
          case '方位': row[gz] = item?.fangwei || '-'; break;
          case '季节': row[gz] = item?.jijie || '-'; break;
          case '纳音': row[gz] = item?.nayin?.nayin_name || '-'; break;
          case '纳音五行': row[gz] = item?.nayin?.nayin_wuxing || '-'; break;
          case '长生状态': row[gz] = item?.nayin?.zhuangtai || '-'; break;
          case '操作': row[gz] = ''; break;
          default: row[gz] = '-';
        }
      });
      return row;
    });
  };

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <Title level={2}>干支对比</Title>

      <Card style={{ marginBottom: 24 }}>
        <Space size="middle" style={{ marginBottom: 16 }}>
          <Select
            mode="multiple"
            placeholder="选择要对比的干支"
            value={selectedGanzhi}
            onChange={setSelectedGanzhi}
            style={{ minWidth: 300 }}
            maxTagCount={4}
          >
            {allGanzhi.map((gz) => (
              <Option key={gz} value={gz}>{gz}</Option>
            ))}
          </Select>
          <Button
            type="primary"
            icon={<SwapOutlined />}
            onClick={handleCompare}
            loading={loading}
          >
            开始对比
          </Button>
        </Space>
        <Text type="secondary">最多可选择10个干支进行对比</Text>
      </Card>

      {compareData.length > 0 && (
        <Card>
          <Table
            columns={columns}
            dataSource={getTableData()}
            pagination={false}
            scroll={{ x: 'max-content' }}
          />
        </Card>
      )}
    </div>
  );
};

export default Compare;
