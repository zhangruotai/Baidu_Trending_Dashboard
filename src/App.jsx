import { useEffect, useState } from "react";
import axios from "axios";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

function App() {
  const [data, setData] = useState([]);

  // 从 Flask API 读取数据库中的数据
  const fetchData = () => {
    axios.get("http://127.0.0.1:5001/api/trending")
      .then(res => {
        setData(res.data.data);
      })
      .catch(err => {
        console.error(err);
      });
  };

  useEffect(() => {
    fetchData();
  }, []);

  const top10Data = data.slice(0, 10);

  const minHotIndex = top10Data.length > 0
    ? Math.min(...top10Data.map(item => item.hot_index))
    : 0;

  const updateTime = data.length > 0 ? data[0].created_at : "";

  return (
    <div style={{ padding: "30px", maxWidth: "1100px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center" }}>
        百度热搜数据可视化
      </h1>

      {updateTime && (
        <p style={{ textAlign: "center", color: "#888", marginBottom: "20px" }}>
          数据更新时间：{updateTime}
        </p>
      )}

      <h2 style={{ textAlign: "center" }}>热搜列表</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginBottom: "40px",
          fontSize: "16px"
        }}
      >
        <thead>
          <tr style={{ backgroundColor: "#f5f5f5" }}>
            <th style={thStyle}>排名</th>
            <th style={thStyle}>热搜标题</th>
            <th style={thStyle}>热搜指数</th>
          </tr>
        </thead>

        <tbody>
          {data.map((item) => (
            <tr key={item.ranking} style={{ borderBottom: "1px solid #eee" }}>
              <td style={rankStyle}>{item.ranking}</td>
              <td style={titleStyle}>{item.title}</td>
              <td style={hotIndexStyle}>
                {item.hot_index.toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2 style={{ textAlign: "center" }}>Top 10 热搜指数图</h2>

      <BarChart width={900} height={400} data={top10Data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="ranking" />

        <YAxis
          width={90}
          domain={[Math.floor(minHotIndex * 0.95), "dataMax"]}
          tickFormatter={(value) => `${(value / 10000).toFixed(0)}万`}
        />

        <Tooltip
         formatter={(value) => [`${value.toLocaleString()}`, "热搜指数"]}
         labelFormatter={(label) => `热搜排名：${label}`}
        />

        <Bar dataKey="hot_index" fill="#ff7300" />
      </BarChart>
    </div>
  );
}

/* ===== 样式 ===== */

const thStyle = {
  padding: "12px",
  textAlign: "left",
  fontWeight: "bold",
  borderBottom: "2px solid #ddd"
};

const rankStyle = {
  padding: "12px",
  width: "80px",
  textAlign: "center",
  fontWeight: "bold"
};

const titleStyle = {
  padding: "12px",
  textAlign: "left"
};

const hotIndexStyle = {
  padding: "12px",
  width: "160px",
  textAlign: "right",
  color: "#ff6600",
  fontWeight: "bold"
};

export default App;