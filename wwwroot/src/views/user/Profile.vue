<template>
  <div class="app-container">
    <div class="btn-primary">
      <el-button type="primary" @click="EditUser(null)">创建</el-button>
    </div>
    <el-dialog class="btn-dialog" :title="form.titleL" :visible.sync="dialogFormVisible">
      <el-form ref="FormRef" :model="form" class="btn-form">
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="form.name" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="登录名" :label-width="formLabelWidth">
          <el-input v-model="form.username" placeholder="请输入登录名" />
        </el-form-item>
        <el-form-item label="登录密码" :label-width="formLabelWidth">
          <el-input v-model="form.password" type="password" autocomplete="off" placeholder="请输入密码" @input="changeValue" />
        </el-form-item>
        <el-form-item label="用户组" :label-width="formLabelWidth">
          <el-select v-model="form.groups_id" class="btn-sel" placeholder="请选择用户组">
            <el-option v-for="item in user_group" :key="item.id" :label="item.name" :value="item.id">{{ item.name }}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="角色名" :label-width="formLabelWidth">
          <el-select v-model="form.role_ac" class="btn-sel" placeholder="请选择角色名">
            <el-option label="管理员" value="admin">管理员</el-option>
            <el-option label="审计员" value="auditor">审计员</el-option>
            <el-option label="用户" value="person">用户</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="激活状态" :label-width="formLabelWidth">
          <el-checkbox v-model="form.is_active">默认勾选</el-checkbox>
          <span v-if=" form.is_active == false" class="btn-active">已被禁用</span>
        </el-form-item>
        <el-form-item label="可信主机" :label-width="formLabelWidth">
          <el-input v-model="form.authip" placeholder="默认为空则表示全部信任,指定IP请使用','分隔" />
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
      <el-table-column label="角色名" align="center">
        <template slot-scope="scope">
          <span v-if=" scope.row.role_ac == 'admin'">管理员</span>
          <span v-else-if=" scope.row.role_ac == 'auditor'">审计员</span>
          <span v-else>用户</span>
        </template>
      </el-table-column>
      <el-table-column label="用户名" align="center">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="登录名" align="center">
        <template slot-scope="scope">
          {{ scope.row.username }}
        </template>
      </el-table-column>
      <el-table-column label="用户组" align="center">
        <template slot-scope="scope">
          {{ scope.row.groups_display }}
        </template>
      </el-table-column>
      <el-table-column label="激活状态" align="center">
        <template slot-scope="scope">
          <span v-if=" scope.row.is_active == true">已激活</span>
          <span v-else>已停用</span>
        </template>
      </el-table-column>
      <!-- <el-table-column label="在线状态" align="center">
        <template slot-scope="scope">
          <span v-if=" scope.row.is_staff == true">在线</span>
          <span v-else>已下线</span>
        </template>
      </el-table-column> -->
      <el-table-column label="创建时间" width="250" align="center">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="300" align="center">
        <template slot-scope="scope">
          <div>
            <el-button type="primary" @click="EditUser(scope.row)">编辑</el-button>
            <el-button v-if="scope.row.is_active == true" type="warning" @click="DelUser(scope.row.id,1)">锁定</el-button>
            <el-button v-else type="success" @click="DelUser(scope.row.id,2)">解锁</el-button>
            <el-button type="danger" @click="DelUser(scope.row.id,0)">删除</el-button>
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
import { isArray } from '@/utils/validate'
import { MessageBox } from 'element-ui'

export default {
  name: 'UserProfile',
  data() {
    return {
      list: null,
      pagination: { page: 1, pageSize: 10, total: 0 },
      listLoading: true,
      dialogFormVisible: false,
      user_group: {},
      form: {
        id: 0,
        titleL: '添加用户',
        username: '',
        name: '',
        password: '',
        is_active: true,
        role_ac: 'person',
        authip: 'all',
        groups_id: 0
      },
      formLabelWidth: '120px'
    }
  },
  created() {
    this.fetchData()
    this.fetchGroup()
  },
  methods: {
    changeValue() {
      this.$forceUpdate()
    },
    fetchGroup() {
      getList('user', 'group').then(data => {
        this.user_group = data.message.results
      })
    },
    fetchData() {
      this.listLoading = true
      getList('user', 'user').then(data => {
        this.list = data.message.results
        this.pagination.total = data.message.count
        this.listLoading = false
      })
    },
    handlePageChange(page) {
      this.pagination.page = page
      this.fetchData()
    },
    EditUser(data) {
      this.dialogFormVisible = true
      if (!data) {
        this.form.id = 0
        this.form.titleL = '添加用户'
        this.form.username = ''
        this.form.name = ''
        this.form.password = ''
        this.form.role_ac = 'person'
        this.form.authip = 'all'
        this.form.is_active = true
        this.form.groups_id = 0
      } else {
        this.form.id = data.id
        this.form.titleL = '编辑用户'
        this.form.username = data.username
        this.form.name = data.name
        this.form.password = ''
        this.form.role_ac = data.role_ac
        this.form.authip = data.authip
        this.form.is_active = data.is_active
        if (isArray(data.groups)) {
          this.form.groups_id = data.groups[0]
        } else {
          this.form.groups_id = data.groups
        }
      }
    },
    DelUser(dataid, type) {
      if (type === 0) {
        MessageBox.confirm('确认是否要删除?', '删除用户', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          destroy('user', 'user', dataid).then(data => {
            this.fetchData()
            this.$message.success('删除成功！')
          }).catch(error => {
            this.$message.error(error)
          })
        })
      } else if (type === 1) {
        MessageBox.confirm('确认是否要停用该用户?', '停用用户', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          update('user', 'user', { 'is_active': false, 'is_saff': false }, dataid).then(data => {
            this.fetchData()
            this.$message.success('停用成功！')
          }).catch(error => {
            this.$message.error(error)
          })
        })
      } else {
        MessageBox.confirm('确认是否要启用该用户?', '启用用户', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          update('user', 'user', { 'is_active': true, 'is_saff': false }, dataid).then(data => {
            this.fetchData()
            this.$message.success('启用成功！')
          }).catch(error => {
            this.$message.error(error)
          })
        })
      }
    },
    Submit() {
      var requestForm = this.form
      this.dialogFormVisible = false
      delete requestForm.titleL
      if (requestForm.password === null || requestForm.password === '') {
        delete requestForm.password
      }
      if (requestForm.id === 0) {
        delete requestForm.id
        post('user', 'user', requestForm).then(data => {
          this.fetchData()
          this.$message.success('提交成功！')
        }).catch(error => {
          this.$message.error(error)
        })
      } else {
        update('user', 'user', requestForm, requestForm.id).then(data => {
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
