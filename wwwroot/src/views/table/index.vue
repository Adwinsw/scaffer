<template>
  <div class="app-container">
    <div class="btn-primary">
      <el-button type="primary" @click="dialogFormVisible = true">创建</el-button>
      <el-dialog title="添加用户" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="用户登录名" :label-width="formLabelWidth">
            <el-input v-model="form.username" autocomplete="off" />
          </el-form-item>
          <el-form-item label="用户名称" :label-width="formLabelWidth">
            <el-input v-model="form.name" autocomplete="off" />
          </el-form-item>
          <el-form-item label="登录密码" :label-width="formLabelWidth">
            <el-input v-model="form.password" autocomplete="off" />
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column label="ID" width="95" align="center">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="序号" width="95" align="center">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="名称" width="180" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="用户" width="180" align="center">
        <template slot-scope="scope">
          {{ scope.row.username }}
        </template>
      </el-table-column>
      <el-table-column label="密码" align="center">
        <template slot-scope="scope">
          {{ scope.row.password }}
        </template>
      </el-table-column>
      <el-table-column label="最后登录时间" width="300" align="center">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.last_login }}</span>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-show="pagination.total > pagination.pageSize"
      :total="pagination.total"
      :page-size="pagination.pageSize"
      :current-page="pagination.page"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script>
import { getList } from '@/api/table'

export default {
  data() {
    return {
      list: null,
      pagination: { page: 1, pageSize: 10, total: 0 },
      listLoading: true,
      dialogFormVisible: false,
      form: {
        username: '',
        name: '',
        password: ''
      },
      formLabelWidth: '120px'
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getList('user').then(data => {
        this.list = data.message.results
        this.pagination.total = data.message.count
        this.listLoading = false
      })
    },
    handlePageChange(page) {
      this.pagination.page = page
      this.fetchData()
    },
    onSubmit() {
      this.$message.success('submit!')
    }
  }
}
</script>
<style lang="scss">
.app-container{
  .btn-primary {
    float: left;
    margin: 0 auto 10px auto;
    .el-button {
      padding: 9px 15px;
    }
  }
}
</style>
