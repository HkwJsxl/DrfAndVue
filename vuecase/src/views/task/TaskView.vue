<template>
  <div>
    <el-menu :default-active="subActiveIndex" class="el-menu-demo sub-menu" mode="horizontal" router>
      <el-menu-item class="el-menu-item" index="activity" :route="{name:'list'}"><i class="el-icon-s-shop"></i>活动管理</el-menu-item>
      <el-menu-item class="el-menu-item" index="promo" :route="{name:'promo'}"><i class="el-icon-s-marketing"></i>推广码</el-menu-item>
      <el-menu-item class="el-menu-item" index="statistics" :route="{name:'statistics'}"><i class="el-icon-s-data"></i>数据统计</el-menu-item>
      <el-menu-item class="el-menu-item" index="fans" :route="{name:'fans'}"><i class="el-icon-s-custom"></i>参与粉丝</el-menu-item>
    </el-menu>

    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "TaskView",
  data() {
    return {
      subActiveIndex: '',
    }
  },
  watch: {
    $route: function (to) {
      this.subActiveIndex = to.matched[2].name;
    }
  },
  mounted() {
    // console.log(this.$route.matched)
    // console.log(this.$route.path)
    // console.log(this.$route.fullPath)
    // 获取当前的所有路由
    // console.log(this.$route)
    this.subActiveIndex = this.$route.matched[2].name;
  }
}
</script>

<style scoped>

</style>