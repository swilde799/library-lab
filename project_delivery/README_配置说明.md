# 数据库与集群配置说明
## 1. 数据文件
- books.txt (50条), readers.txt (30条), borrow_logs.txt (3000条)
- category_stats.json (分类统计导出文件)

## 2. 单机部署
- 端口：27017，配置见 `single.conf`

## 3. 副本集部署 (高可用)
- 27017 (PRIMARY), 27018 (SECONDARY), 27019 (SECONDARY)
- 统一 keyFile 认证

## 4. 分片集群部署 (水平扩展)
- 配置服务器：27020
- 分片1：27021，分片2：27022
- 路由节点 (mongos)：27023
