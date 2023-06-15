<template>
  <div class="app-container">
    <div class="btn-primary">
      <el-button type="primary" @click="EditGroup(null)">创建</el-button>
    </div>
    <el-dialog class="btn-dialog" :title="form.titleL" :visible.sync="dialogFormVisible">
      <el-form ref="FormRef" :model="form" class="btn-form">
        <el-form-item label="组名" :label-width="formLabelWidth">
          <el-input v-model="form.name" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="选择用户" :label-width="formLabelWidth">
          <el-select v-model="form.users" class="btn-sel" placeholder="请选择用户">
            <el-option v-for="item in user_list" :key="item.id" :label="item.username" :value="item.id">{{ item.username }}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注" :label-width="formLabelWidth">
          <el-input v-model="form.comment" placeholder="" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="Submit">确 定</el-button>
      </div>
    </el-dialog>
    <el-table
      v-loading="listLoading"
      class="btn-table"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column label="序号" align="center">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
      <el-table-column label="组名" align="center">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="备注" align="center">
        <template slot-scope="scope">
          {{ scope.row.comment }}
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="250" align="center">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="300" align="center">
        <template slot-scope="scope">
          <div>
            <el-button type="primary" @click="EditGroup(scope.row)">编辑</el-button>
            <el-button type="danger" @click="DelGroup(scope.row.id)">删除</el-button>
          </div>
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
import { getList, post, update, destroy } from '@/api/table'
import { MessageBox } from 'element-ui'

export default {
  name: 'UserGroup',
  data() {
    return {
      list: null,
      pagination: { page: 1, pageSize: 10, total: 0 },
      listLoading: true,
      dialogFormVisible: false,
      user_list: {},
      form: {
        id: 0,
        titleL: '添加组',
        name: '',
        comment: '',
        users: null
      },
      formLabelWidth: '120px'
    }
  },
  created() {
    this.fetchData()
    this.fetchUser()
  },
  methods: {
    fetchUser() {
      getList('user', 'user').then(data => {
        this.user_list = data.message.results
      })
    },
    fetchData() {
      this.listLoading = true
      getList('user', 'group').then(data => {
        this.list = data.message.results
        this.pagination.total = data.message.count
        this.listLoading = false
      })
    },
    handlePageChange(page) {
      this.pagination.page = page
      this.fetchData()
    },
    EditGroup(data) {
      console.log(data)
      if (!data) {
        this.form.id = 0
        this.form.titleL = '添加组'
        this.form.name = ''
        this.form.comment = ''
        this.form.users = null
      } else {
        this.form.id = data.id
        this.form.titleL = '编辑组'
        this.form.name = data.name
        this.form.comment = data.comment
        this.form.users = data.users
      }
      this.dialogFormVisible = true
    },
    DelGroup(dataid) {
      MessageBox.confirm('确认是否要删除?', '删除组', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        destroy('user', 'group', dataid).then(data => {
          this.fetchData()
          this.$message.success('删除成功！')
        }).catch(error => {
          this.$message.error(error)
        })
      })
    },
    Submit() {
      this.dialogFormVisible = false
      delete this.form.title
      if (this.form.id === 0) {
        delete this.form.id
        post('user', 'group', this.form).then(data => {
          this.fetchData()
          this.$message.success('提交成功！')
        }).catch(error => {
          this.$message.error(error)
        })
      } else {
        update('user', 'group', this.form, this.form.id).then(data => {
          this.fetchData()
          this.$message.success('提交成功！')
        }).catch(error => {
          this.$message.error(error)
        })
      }
    }
  }
}
</script>
  <style lang="scss" scoped>
  .app-container{
    .btn-primary {
      float: left;
      margin: 0 auto 10px auto;
      .el-button {
        padding: 9px 15px;
      }
    }
    .btn-dialog {
      .btn-sel {
        width:100%;
      }
      .el-button {
        padding: 9px 15px;
      }
      .btn-active{
        margin-left: 10px;
        color: red;
      }
    }
    .btn-table{
      .el-button {
        font-size: 14px;
        padding: 5px 10px;
      }
    }
  }
  </style>

