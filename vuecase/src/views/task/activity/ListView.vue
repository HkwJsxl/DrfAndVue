<template>
  <div style="margin: 24px">
    <router-link :to="{name:'create'}">
      <el-button type="primary" size="medium"><i class="el-icon-plus"></i> 新建活动</el-button>
    </router-link>

    <el-card class="box-card">
      <el-form label-width="80px" :inline="true" size="medium" :model="searchForm" ref="searchForm">
        <el-form-item label="活动名称" prop="name">
          <el-input placeholder="活动名称" v-model="searchForm.name"></el-input>
        </el-form-item>
        <el-form-item label="公众号" prop="mobile">
          <el-select placeholder="公众号" v-model="searchForm.mobile">
            <el-option v-for="item in searchFormMobile" :key="item.value" :label="item.label"
                       :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="活动状态" prop="status">
          <el-select placeholder="活动状态" v-model="searchForm.status">
            <el-option v-for="item in searchFormStatus" :key="item.value" :label="item.label"
                       :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button size="medium" @click="startSearch">筛选</el-button>
          <el-button size="medium" @click="resetSearchForm('searchForm')">重置</el-button>
        </el-form-item>
      </el-form>

    </el-card>

    <el-row :gutter="20">
      <el-col style="width: 240px;margin-bottom: 20px;" v-for="(o, index) in 12" :key="o">
        <el-card>
          <img src="../../../assets/img/img.jpg" class="image" alt="图片">
          <div style="padding: 14px;font-size: 14px">
            <span>私聊+V---{{ index }}</span>
            <el-row style="margin-top: 8px;">
              <el-button icon="el-icon-search" size="mini" circle></el-button>
              <el-button icon="el-icon-edit" size="mini" circle></el-button>
              <el-button icon="el-icon-check" size="mini" circle></el-button>
              <el-button icon="el-icon-message" size="mini" circle></el-button>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "ListView",
  data() {
    return {
      searchForm: {
        name: '',
        status: [],
        mobile: [],
      },
      searchFormMobile: [
        {label: 'luffy1', value: '1'},
        {label: 'luffy2', value: '2'},
        {label: 'luffy3', value: '3'},
      ],
      searchFormStatus: [
        {label: '正常', value: '0'},
        {label: '异常', value: '1'},
      ],
    }
  },
  methods: {
    startSearch() {
      console.log(this.searchForm);
    },
    resetSearchForm(formName) {
      this.$refs[formName].resetFields();
      console.log(formName);
    },

  }
}
</script>

<style scoped>
.image {
  width: 100%;
  display: block;
  height: 160px;
}

</style>
