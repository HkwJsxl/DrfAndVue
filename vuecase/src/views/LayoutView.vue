<template>
  <div>
    <div>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" router>
        <el-menu-item>媒体宝系统</el-menu-item>
        <el-menu-item index="task" :route="{name: 'list'}">任务宝</el-menu-item>
        <el-menu-item index="msg" :route="{name: 'push'}">消息宝</el-menu-item>
        <el-menu-item index="auth" :route="{name: 'auth'}">公众号授权</el-menu-item>

        <el-submenu index="user" style="float: right;">
          <template slot="title">{{ username }}</template>
          <el-menu-item index="user-1">个人中心</el-menu-item>
          <el-menu-item index="user-2">注销</el-menu-item>
        </el-submenu>
      </el-menu>
    </div>
    <div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: "LayoutView",
  data() {
    return {
      activeIndex: '',
      routers: []
    }
  },
  mounted() {
    // console.log(this.$route.matched)
    // console.log(this.$route.path)
    // console.log(this.$route.fullPath)
    // 获取当前的所有路由
    // console.log(this.$route)
    // console.log(this.$route.matched)
    // 所有路由（先导入router）
    // console.log(router.options.routes)
    this.activeIndex = this.$route.matched[1].name;
  },
  computed: {
    username() {
      return this.$store.state.username;
    }
  }
}
</script>

<style scoped>

</style>