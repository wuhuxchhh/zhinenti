# ============================================================
# 光合日程AI 项目 —— 项目级 shell 环境
# 使用方式：在需要时手动加载
#     source /c/zhinenti/znenv.sh
# 或加入该项目自己的启动脚本；不再全局自动加载，避免影响其它项目。
# ============================================================

# 项目根目录
export ZNHOME="C:/zhinenti"
export COMPDIR="$ZNHOME/competition"
export PATH="/d/texlive/2026/bin/windows:/c/ffmpeg/ffmpeg-8.1.1-full_build/bin:$PATH"

# Python 解释器
alias py="/c/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe"

# --- 编译技术文档 PDF（双遍） ---
techpdf() {
    local dir="${1:-$COMPDIR}"
    echo "[techpdf] Compiling technical_report.tex in $dir ..."
    cd "$dir" || return 1
    xelatex -interaction=nonstopmode technical_report.tex >/dev/null 2>&1
    xelatex -interaction=nonstopmode technical_report.tex
    if [ -f technical_report.pdf ]; then
        local size=$(stat -c%s technical_report.pdf 2>/dev/null || wc -c < technical_report.pdf)
        local pages=$(pdfinfo technical_report.pdf 2>/dev/null | grep "Pages:" | awk '{print $2}')
        echo "[techpdf] Done: ${pages} pages, $(numfmt --to=iec --suffix=B $size 2>/dev/null || echo ${size} bytes)"
    else
        echo "[techpdf] FAILED - check .log"
    fi
}

# --- 重生成所有 matplotlib 技术图 ---
genfigs() {
    local script="${1:-$COMPDIR/gen_all_figs_zh.py}"
    if [ ! -f "$script" ]; then
        echo "[genfigs] Script not found: $script"
        return 1
    fi
    echo "[genfigs] Running $script ..."
    /c/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe "$script"
}

# --- 重生成单张图（需修改脚本后调用） ---
genfig() {
    local name="$1"
    if [ -z "$name" ]; then
        echo "Usage: genfig <name>"
        echo "  e.g. genfig architecture"
        echo "Available: architecture, gesture_flowchart, fatigue_curve, i2c_topology, pomodoro_state, posture_zones, data_protocol, led_feedback, wiring, startup_sequence, rtc_timing, resource_usage, dataflow, edge_vs_cloud"
        return 1
    fi
    # 编辑 gen_all_figs_zh.py，注释掉其他图后运行
    # 或用 grep/sed 临时禁用其他
    echo "[genfig] Regen single: fig_$name.png"
    echo "  提示：单张重生成可通过临时编辑 gen_all_figs_zh.py"
    echo "        在 plt.close() 后加 'if True:' 包裹需要的即可"
}

# --- 查看技术图（用 Windows 默认图片查看器）---
showfig() {
    local name="$1"
    if [ -z "$name" ]; then
        start "$COMPDIR/figs"
        return 0
    fi
    start "$COMPDIR/figs/fig_${name}.png"
}

# --- 打开技术文档 PDF ---
techdoc() {
    start "$COMPDIR/technical_report.pdf"
}

# --- 一键录制验证视频（启动 OBS）---
recvideo() {
    echo "[recvideo] 启动 OBS Studio..."
    if command -v obs &> /dev/null; then
        obs &
    else
        echo "  OBS 未安装。运行: winget install OBSProject.OBSStudio"
        echo "  或使用 Win+Alt+R（Xbox Game Bar）"
    fi
}

# --- 查看项目状态 ---
znstatus() {
    echo "=== 光合日程AI 项目状态 ==="
    if [ -f "$COMPDIR/technical_report.pdf" ]; then
        local size=$(stat -c%s "$COMPDIR/technical_report.pdf" 2>/dev/null || wc -c < "$COMPDIR/technical_report.pdf")
        local pages=$(pdfinfo "$COMPDIR/technical_report.pdf" 2>/dev/null | grep "Pages:" | awk '{print $2}')
        echo "  PDF: ${pages:-?} 页, ${size} 字节"
    else
        echo "  PDF: 未生成 (运行 techpdf)"
    fi
    echo "  图数: $(ls $COMPDIR/figs/ 2>/dev/null | wc -l) 个"
    echo "  Skills: $(ls $ZNHOME/.agents/skills/ 2>/dev/null | wc -l) 个"
}

# --- 提示信息 ---
echo ""
echo "  光合日程AI 项目已加载。可用命令:"
echo "    techpdf    - 编译技术文档 PDF"
echo "    genfigs    - 重生成全部技术图"
echo "    genfig N   - 重生成单张图 (N=architecture/...)"
echo "    showfig N  - 打开技术图"
echo "    techdoc    - 打开 PDF"
echo "    recvideo   - 启动 OBS 录制"
echo "    znstatus   - 项目状态"
echo ""
