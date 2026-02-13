import { useState, useEffect } from 'react';
import { Card, Input, Table, Typography, Spin, message, Tag, Modal } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import * as api from '../services/api';

const { Title, Text } = Typography;

const Shensha = () => {
  const [loading, setLoading] = useState(true);
  const [shenshaList, setShenshaList] = useState([]);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [selectedShensha, setSelectedShensha] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  useEffect(() => {
    loadShenshaList();
  }, []);

  const loadShenshaList = async () => {
    try {
      setLoading(true);
      const response = await api.getShenshaList({ page: 1, page_size: 100 });
      setShenshaList(response.data.items || response.data);
    } catch (error) {
      message.error('加载失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (keyword) => {
    setSearchKeyword(keyword);
    try {
      setLoading(true);
      const response = await api.getShenshaList({ q: keyword, page: 1, page_size: 100 });
      setShenshaList(response.data.items || response.data);
    } catch (error) {
      message.error('搜索失败');
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetail = async (record) => {
    try {
      const response = await api.getShenshaDetail(record.name);
      setSelectedShensha(response.data);
      setModalVisible(true);
    } catch (error) {
      message.error('加载详情失败');
    }
  };

  const columns = [
    {
      title: '神煞名称',
      dataIndex: 'name',
      key: 'name',
      render: (text) => <a onClick={() => handleViewDetail({ name: text })}>{text}</a>,
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (text) => <Tag>{text}</Tag>,
    },
    {
      title: '吉凶',
      dataIndex: 'jixiong',
      key: 'jixiong',
      render: (text) => (
        <Tag color={text === '吉' ? 'green' : text === '凶' ? 'red' : 'orange'}>
          {text}
        </Tag>
      ),
    },
    {
      title: '查法',
      dataIndex: 'check_method',
      key: 'check_method',
      ellipsis: true,
    },
  ];

  if (loading && !shenshaList.length) {
    return (
      <div style={{ textAlign: 'center', padding: 48 }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <Title level={2}>神煞字典</Title>

      <Card style={{ marginBottom: 24 }}>
        <Input.Search
          placeholder="搜索神煞名称"
          allowClear
          enterButton={<SearchOutlined />}
          onSearch={handleSearch}
          style={{ maxWidth: 400 }}
        />
      </Card>

      <Card>
        <Table
          columns={columns}
          dataSource={shenshaList}
          rowKey="id"
          pagination={{ pageSize: 10 }}
          loading={loading}
        />
      </Card>

      <Modal
        title={selectedShensha?.name}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={600}
      >
        {selectedShensha && (
          <div>
            <p><Text type="secondary">类型：</Text>{selectedShensha.type}</p>
            <p><Text type="secondary">吉凶：</Text>{selectedShensha.jixiong}</p>
            <p><Text type="secondary">查法：</Text>{selectedShensha.check_method}</p>
            <p><Text type="secondary">原文：</Text>{selectedShensha.yuanwen}</p>
            <p><Text type="secondary">现代解读：</Text>{selectedShensha.modern_desc}</p>
            <p><Text type="secondary">备注：</Text>{selectedShensha.remark}</p>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Shensha;
