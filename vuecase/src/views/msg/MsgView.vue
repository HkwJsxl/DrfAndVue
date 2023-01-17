<template>
  <div>
    <el-menu :default-active="subActiveIndex" class="el-menu-demo sub-menu" mode="horizontal" router>
      <el-menu-item class="el-menu-item" index="push" :route="{name:'push'}"><i class="el-icon-s-shop"></i>消息推送</el-menu-item>
      <el-menu-item class="el-menu-item" index="sop" :route="{name:'sop'}"><i class="el-icon-s-marketing"></i>sop计划</el-menu-item>
    </el-menu>

    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "MsgView",
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