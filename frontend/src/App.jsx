import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import Home from './pages/Home';
import GanzhiDetail from './pages/GanzhiDetail';
import Compare from './pages/Compare';
import Nayin from './pages/Nayin';
import Shensha from './pages/Shensha';
import Guanxi from './pages/Guanxi';
import Admin from './pages/Admin';
import './App.css';

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ganzhi/:ganzhi" element={<GanzhiDetail />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/nayin" element={<Nayin />} />
          <Route path="/nayin/status/:status" element={<Nayin />} />
          <Route path="/shensha" element={<Shensha />} />
          <Route path="/guanxi" element={<Guanxi />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App;
