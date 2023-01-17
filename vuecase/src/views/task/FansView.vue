<template>
  <div style="margin: 24px">
    <el-card class="box-card">
      <el-form label-width="80px" :inline="true" size="medium" :model="searchForm" ref="searchForm">
        <el-form-item label="当前任务" prop="task">
          <el-select placeholder="任务" v-model="searchForm.task">
            <el-option v-for="item in taskOptions" :key="item.value" :label="item.label"
                       :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="推广码" prop="code">
          <el-select placeholder="推广码" v-model="searchForm.code">
            <el-option v-for="item in codeOptions" :key="item.value" :label="item.label"
                       :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-button size="medium" @click="startSearch">筛选</el-button>
        <el-button size="medium" @click="resetSearchForm('searchForm')">重置</el-button>
      </el-form>
    </el-card>

    <el-card class="box-card">
      <el-row type="flex" justify="end" style="float: right; z-index: 1">
        <el-input placeholder="请输入内容" prefix-icon="el-icon-search" v-model="searchInput" style="margin-right: 10px"
                  size="small"></el-input>
        <el-button size="small" type="primary">导出</el-button>
        <el-button size="small" type="primary" @click="addToBlackList">加入黑名单</el-button>
        <el-button size="small" type="primary">移除黑名单</el-button>
      </el-row>

      <el-tabs type="card" v-model="activeName" @tab-click="handleTabClick">
        <el-tab-pane label="参与用户" name="参与用户">
          <el-table :data="tableData" ref="multipleTable"
                    style="width: 100%" size="medium" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"></el-table-column>
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
                <el-button type="text" @click="confirmDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination style="margin:24px 0;float: right" background layout="prev, pager, next, jumper"
                         :total="pageInfo.totalCount"
                         :page-size="pageInfo.perPageSize" @current-change="currentPage">
          </el-pagination>
        </el-tab-pane>

        <el-tab-pane label="黑名单" name="黑名单">
          <el-table :data="tableBlackData" ref="multipleTable"
                    style="width: 100%" size="medium" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"></el-table-column>
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
                <el-button type="text" @click="confirmDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination style="margin:24px 0;float: right" background layout="prev, pager, next, jumper"
                         :total="pageInfo.totalCount"
                         :page-size="pageInfo.perPageSize" @current-change="currentPage">
          </el-pagination>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!--      <el-tabs v-model="activeName" type="card">-->
    <!--        <el-tab-pane label="参与用户" name="first">-->

    <!--          <el-table ref="myTable" :data="tableData" style="width: 100%"-->
    <!--                    @selection-change="handleSelectionChange">-->
    <!--            <el-table-column type="selection" width="55"></el-table-column>-->
    <!--            <el-table-column prop="date" label="日期"></el-table-column>-->
    <!--            <el-table-column prop="name" label="姓名"></el-table-column>-->
    <!--            <el-table-column prop="address" label="地址"></el-table-column>-->
    <!--            <el-table-column label="状态">-->
    <!--              <template slot-scope="scope">-->
    <!--                <el-tag v-if="scope.row.status === 1" type="success">成功</el-tag>-->
    <!--                <el-tag v-else type="danger">失败</el-tag>-->
    <!--              </template>-->
    <!--            </el-table-column>-->
    <!--            <el-table-column label="操作">-->
    <!--              <template slot-scope="scope">-->
    <!--                <el-button @click="handleSelectionChange(scope.row)" type="text" size="small">查看</el-button>-->

    <!--                <el-popconfirm title="这是一段内容确定删除吗？" @confirm="confirmDelete(scope.row)">-->
    <!--                  <el-button slot="reference" type="text" size="small">删除</el-button>-->
    <!--                </el-popconfirm>-->
    <!--              </template>-->
    <!--            </el-table-column>-->
    <!--          </el-table>-->

    <!--        </el-tab-pane>-->


    <!--        <el-tab-pane label="黑名单" name="second">-->
    <!--          <el-table :data="tableData" border style="width: 100%">-->
    <!--            <el-table-column prop="date" label="日期"></el-table-column>-->
    <!--            <el-table-column prop="name" label="姓名"></el-table-column>-->
    <!--            <el-table-column prop="address" label="地址"></el-table-column>-->
    <!--            <el-table-column label="状态">-->
    <!--              <template slot-scope="scope">-->
    <!--                <el-tag v-if="scope.row.status === 1" type="success">成功</el-tag>-->
    <!--                <el-tag v-else type="danger">失败</el-tag>-->
    <!--              </template>-->
    <!--            </el-table-column>-->
    <!--            <el-table-column label="操作">-->
    <!--              <template slot-scope="scope">-->
    <!--                <el-button @click="handleSelectionChange(scope.row)" type="text" size="small">查看</el-button>-->

    <!--                <el-popconfirm title="这是一段内容确定删除吗？" @confirm="confirmDelete(scope.row)">-->
    <!--                  <el-button slot="reference" type="text" size="small">删除</el-button>-->
    <!--                </el-popconfirm>-->
    <!--              </template>-->
    <!--            </el-table-column>-->
    <!--          </el-table>-->
    <!--        </el-tab-pane>-->
    <!--      </el-tabs>-->
    <!--    </el-card>-->

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
  name: "FansView",
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
      tableBlackData:
          [{
            date: '2016-05-01',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1519 弄',
            status: 1,
          }],
      taskOptions: [
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
      codeOptions: [
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
        task: '',
        code: '',
      },
      pageInfo: {
        totalCount: 1000,
        perPageSize: 2,
      },
      dialogVisible: false,
      returnForm: {
        x1: '',
        x2: '',
      },
      activeName: '参与用户',
      searchInput: '',
      selectDataList: [],
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
    handleTabClick(tab, event) {
      console.log(tab, event);
    },
    handleSelectionChange(valueList) {
      console.log(valueList);
      this.selectDataList = valueList;
    },
    addToBlackList() {
      console.log('加入黑名单', this.selectDataList);
    }
  }
}
</script>

<style scoped>
.box-card {
  margin: 24px 0;
}
</style>
