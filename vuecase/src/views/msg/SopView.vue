<template>
  <div style="margin: 24px">
    <el-card class="box-card">
      <el-form label-width="80px" :inline="true" size="medium" :model="searchForm" ref="searchForm">
        <el-form-item label="标题" prop="title">
          <el-input v-model="searchForm.title" placeholder="标题"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="category">
          <el-select placeholder="请选择类型" v-model="searchForm.category">
            <el-option v-for="item in categoryOptions" :key="item.value" :label="item.label"
                       :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-button size="medium" @click="startSearch">筛选</el-button>
        <el-button size="medium" @click="resetSearchForm('searchForm')">重置</el-button>
      </el-form>
    </el-card>

    <el-card class="box-card">
      <div slot="header" class="clearfix" style="margin-bottom: 10px">
        <span><i class="el-icon-s-grid"></i> 消息列表</span>
        <el-button style="float: right;" type="primary" size="medium" @click="addDialog">
          <i class="el-icon-circle-plus-outline"></i> 新建推送
        </el-button>
      </div>

      <el-table :data="tableData" border style="width: 100%" size="medium">
        <el-table-column prop="date" label="日期"></el-table-column>
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column prop="address" label="地址"></el-table-column>
        <el-table-column prop="status" label="状态">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.status === 0" type="success">成功</el-tag>
            <el-tag v-else type="danger">失败</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button @click="searchClick(scope.row)" type="text">查看</el-button>
            <!--            <el-popconfirm title="确定删除吗?" @confirm="confirmDelete(scope.row)">-->
            <!--              <el-button slot="reference" type="text">删除</el-button>-->
            <!--            </el-popconfirm>-->
            <el-button type="text" @click="confirmDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin:24px 0;float: right" background layout="prev, pager, next, jumper"
                     :total="pageInfo.totalCount"
                     :page-size="pageInfo.perPageSize" @current-change="currentPage">
      </el-pagination>
    </el-card>


    <el-dialog title="收货地址" :visible.sync="dialogFormVisible">
      <el-form label-position="left" label-width="80px" :model="returnForm">
        <el-form-item label="名称" prop="x1">
          <el-input autocomplete="off" v-model="returnForm.x1"></el-input>
        </el-form-item>
        <el-form-item label="区域" prop="x2">
          <el-select placeholder="请选择区域" v-model="returnForm.x2">
            <el-option label="北京" value="shanghai"></el-option>
            <el-option label="上海" value="beijing"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="提示" :visible.sync="dialogVisible" width="30%">
      <span>这是一段信息</span>
      <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
              </span>
    </el-dialog>

  </div>
</template>

<script>
export default {
  name: "SopView",
  data() {
    return {
      tableData: [{
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄',
        status: 0,
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1517 弄',
        status: 0,
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1519 弄',
        status: 1,
      }, {
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1516 弄',
        status: 0,
      }],
      categoryOptions: [
        {
          value: '1',
          label: '黄金糕'
        }, {
          value: '2',
          label: '双皮奶'
        }, {
          value: '3',
          label: '蚵仔煎'
        }, {
          value: '4',
          label: '龙须面'
        }, {
          value: '5',
          label: '北京烤鸭'
        }],
      searchForm: {
        title: '',
        category: '',
        promoDateTime: '',
      },
      pageInfo: {
        totalCount: 1000,
        perPageSize: 2,
      },
      dialogFormVisible: false,
      dialogVisible: false,
      returnForm: {
        x1: '',
        x2: '',
      },
    }
  },
  methods: {
    searchClick(formRow) {
      this.dialogVisible = true;
      console.log(formRow);
    },
    confirmDelete(formRow) {
      console.log(formRow);

      this.$confirm('此操作将永久删除该文件, 是否继续?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '删除成功!'
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });

    },
    startSearch() {
      console.log(this.searchForm);
    },
    resetSearchForm(formName) {
      this.$refs[formName].resetFields();
      console.log(formName);
    },
    currentPage(pageNum) {
      console.log(pageNum);
    },
    addDialog() {
      this.dialogFormVisible = true;
    },
  }
}
</script>

<style scoped>
.box-card {
  margin: 24px 0;
}
</style>
