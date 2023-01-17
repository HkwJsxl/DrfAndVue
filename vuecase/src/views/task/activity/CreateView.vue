<template>
  <div style="margin: 24px">
    <el-row type="flex" justify="end">
      <el-button type="success" size="medium"><i class="el-icon-setting"></i> 保存</el-button>
    </el-row>
    <el-tabs tab-position="left" v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="活动设置" name="tab1">活动设置</el-tab-pane>
      <el-tab-pane label="参与公众号" name="tab2">参与公众号</el-tab-pane>
      <el-tab-pane label="奖励设置" name="tab3">奖励设置</el-tab-pane>
      <el-tab-pane label="海报设置" name="tab4">海报设置</el-tab-pane>
      <el-tab-pane label="进度消息" name="tab5">进度消息</el-tab-pane>
      <el-tab-pane label="其他消息" name="tab6">其他消息</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: "CreateView",
  data() {
    return {
      activeName: 'tab1'
    }
  },
  methods: {
    handleClick(e) {
      console.log(e);
    },
  },
  created() {
    const loading = this.$loading({
      lock: true,
      text: '加载中...',
      spinner: 'el-icon-loading',
      background: 'rgba(0, 0, 0, 0.7)'
    });
    setTimeout(() => {
      loading.close();
    }, 1000);
  }
}
</script>

<style scoped>

</style>