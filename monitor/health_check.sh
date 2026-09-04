#!/bin/bash
# MCP Server 健康检查 + 告警
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
# 检查: ① 8848 端口监听 ② MCP 进程存活 ③ 关键工程化资产存在
# 用法: ./health_check.sh   (crontab 每 5 分钟调用)
# 异常时: 日志 + macOS 通知 + 退出码 1

PORT=8848
LOG="/Users/donglai/Doubao/chats/2026-09-03/new-chat-6/monitor/mcp-health.log"
SERVER_PY="/Users/donglai/Doubao/chats/2026-09-03/new-chat-6/vscode-mcp/server.py"
SKILL_DIR="/Users/donglai/Library/Application Support/Doubao/Default/.doubao/agent_mode/workspace/.user_skills"
NOW=$(date "+%Y-%m-%d %H:%M:%S")
FAILS=0

mkdir -p "$(dirname "$LOG")"
log() { echo "[$NOW] $1" >> "$LOG"; }

# ① 端口
if lsof -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; then
  log "✓ 端口 $PORT 监听正常"
else
  log "✗ 端口 $PORT 未监听（MCP Server 可能挂了）"; FAILS=$((FAILS+1))
fi

# ② 进程
if pgrep -f "server.py" >/dev/null 2>&1; then
  log "✓ MCP 进程存活 ($(pgrep -f server.py | tr '\n' ' '))"
else
  log "✗ MCP 进程不存在"; FAILS=$((FAILS+1))
fi

# ③ 关键资产
[ -f "$SERVER_PY" ] && log "✓ server.py 存在" || { log "✗ server.py 丢失"; FAILS=$((FAILS+1)); }
[ -d "$SKILL_DIR" ] && log "✓ 技能目录存在 ($(ls -d "$SKILL_DIR"/*/ 2>/dev/null | wc -l | tr -d ' ') 个)" || { log "✗ 技能目录丢失"; FAILS=$((FAILS+1)); }

# ④ 远端仓库可达（配置管理健康）
ROOT="/Users/donglai/Doubao/chats/2026-09-03/new-chat-6"
if timeout 10 gh api repos/Eastdongjun/doubao-eng-control-plane -q .default_branch >/dev/null 2>&1; then
  log "✓ GitHub 远端可达 (gh api)"
elif GIT_TERMINAL_PROMPT=0 timeout 10 git -C "$ROOT" ls-remote origin -h refs/heads/main >/dev/null 2>&1; then
  log "✓ GitHub 远端可达 (git)"
else
  log "✗ GitHub 远端不可达（网络/认证）"; FAILS=$((FAILS+1))
fi

if [ $FAILS -gt 0 ]; then
  log "✗✗ 健康检查失败 $FAILS 项 → 发送告警"
  osascript -e "display notification \"MCP 监控告警: $FAILS 项异常（$(date '+%H:%M')）\" with title \"豆包工程化监控\" sound name \"Funk\"" 2>/dev/null
  exit 1
else
  log "✓ 全部健康"
  exit 0
fi
