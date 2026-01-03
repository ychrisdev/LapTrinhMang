import express from 'express';
import db from '../config/database.js';
import { authMiddleware } from '../middlewares/auth.js';
import { upload } from '../middlewares/upload.js';
import fs from 'fs';
import path from 'path';

const router = express.Router();

// PUBLIC: Lấy danh sách blogs (có tìm kiếm & sắp xếp)
router.get('/', async (req, res) => {
  try {
    const { search = '', sort = 'created_at' } = req.query;
    
    let query = `
      SELECT 
        b.id, 
        b.title, 
        b.content, 
        b.image, 
        b.user_id,
        b.created_at, 
        b.updated_at,
        u.name as author_name
      FROM blogs b
      JOIN users u ON b.user_id = u.id
    `;
    
    const params = [];
    
    if (search) {
      query += ' WHERE b.title LIKE ? OR b.content LIKE ?';
      params.push(`%${search}%`, `%${search}%`);
    }
    
    // Sắp xếp
    const validSorts = ['created_at', 'title', 'updated_at'];
    const sortColumn = validSorts.includes(sort) ? sort : 'created_at';
    query += ` ORDER BY b.${sortColumn} DESC`;
    
    const [blogs] = await db.query(query, params);
    
    res.json({
      success: true,
      data: blogs
    });
  } catch (error) {
    console.error('Lỗi lấy danh sách blogs:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi server'
    });
  }
});

// PUBLIC: Lấy chi tiết 1 blog
router.get('/:id', async (req, res) => {
  try {
    const [blogs] = await db.query(
      `SELECT 
        b.id, 
        b.title, 
        b.content, 
        b.image, 
        b.user_id,
        b.created_at, 
        b.updated_at,
        u.name as author_name,
        u.email as author_email
      FROM blogs b
      JOIN users u ON b.user_id = u.id
      WHERE b.id = ?`,
      [req.params.id]
    );
    
    if (blogs.length === 0) {
      return res.status(404).json({
        success: false,
        message: 'Không tìm thấy blog'
      });
    }
    
    res.json({
      success: true,
      data: blogs[0]
    });
  } catch (error) {
    console.error('Lỗi lấy chi tiết blog:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi server'
    });
  }
});

// PRIVATE: Tạo blog mới
router.post('/', authMiddleware, upload.single('image'), async (req, res) => {
  try {
    const { title, content } = req.body;
    const userId = req.user.id;
    
    // Validate
    if (!title || !content) {
      return res.status(400).json({
        success: false,
        message: 'Tiêu đề và nội dung không được để trống'
      });
    }
    
    // Lấy tên file nếu có upload
    const imagePath = req.file ? req.file.filename : null;
    
    const [result] = await db.query(
      'INSERT INTO blogs (title, content, image, user_id) VALUES (?, ?, ?, ?)',
      [title, content, imagePath, userId]
    );
    
    // Lấy blog vừa tạo
    const [newBlog] = await db.query(
      `SELECT 
        b.*, 
        u.name as author_name
      FROM blogs b
      JOIN users u ON b.user_id = u.id
      WHERE b.id = ?`,
      [result.insertId]
    );
    
    res.status(201).json({
      success: true,
      message: 'Tạo blog thành công',
      data: newBlog[0]
    });
  } catch (error) {
    console.error('Lỗi tạo blog:', error);
    
    // Xóa file đã upload nếu có lỗi
    if (req.file) {
      fs.unlinkSync(req.file.path);
    }
    
    res.status(500).json({
      success: false,
      message: 'Lỗi server khi tạo blog'
    });
  }
});

// PRIVATE: Cập nhật blog
router.put('/:id', authMiddleware, upload.single('image'), async (req, res) => {
  try {
    const { title, content, removeImage } = req.body;
    const blogId = req.params.id;
    const userId = req.user.id;
    
    // Kiểm tra blog có tồn tại và thuộc về user không
    const [blogs] = await db.query(
      'SELECT * FROM blogs WHERE id = ?',
      [blogId]
    );
    
    if (blogs.length === 0) {
      return res.status(404).json({
        success: false,
        message: 'Không tìm thấy blog'
      });
    }
    
    if (blogs[0].user_id !== userId) {
      return res.status(403).json({
        success: false,
        message: 'Bạn không có quyền chỉnh sửa blog này'
      });
    }
    
    const oldBlog = blogs[0];
    let imagePath = oldBlog.image;
    
    // Xử lý hình ảnh
    if (req.file) {
      // Có upload hình mới
      imagePath = req.file.filename;
      
      // Xóa hình cũ
      if (oldBlog.image) {
        const oldImagePath = path.join('uploads', oldBlog.image);
        if (fs.existsSync(oldImagePath)) {
          fs.unlinkSync(oldImagePath);
        }
      }
    } else if (removeImage === 'true') {
      // Xóa hình hiện tại
      if (oldBlog.image) {
        const oldImagePath = path.join('uploads', oldBlog.image);
        if (fs.existsSync(oldImagePath)) {
          fs.unlinkSync(oldImagePath);
        }
      }
      imagePath = null;
    }
    
    // Cập nhật database
    await db.query(
      'UPDATE blogs SET title = ?, content = ?, image = ? WHERE id = ?',
      [title, content, imagePath, blogId]
    );
    
    // Lấy blog đã cập nhật
    const [updatedBlog] = await db.query(
      `SELECT 
        b.*, 
        u.name as author_name
      FROM blogs b
      JOIN users u ON b.user_id = u.id
      WHERE b.id = ?`,
      [blogId]
    );
    
    res.json({
      success: true,
      message: 'Cập nhật blog thành công',
      data: updatedBlog[0]
    });
  } catch (error) {
    console.error('Lỗi cập nhật blog:', error);
    
    // Xóa file mới upload nếu có lỗi
    if (req.file) {
      fs.unlinkSync(req.file.path);
    }
    
    res.status(500).json({
      success: false,
      message: 'Lỗi server khi cập nhật blog'
    });
  }
});

// PRIVATE: Xóa blog
router.delete('/:id', authMiddleware, async (req, res) => {
  try {
    const blogId = req.params.id;
    const userId = req.user.id;
    
    // Kiểm tra blog có tồn tại và thuộc về user không
    const [blogs] = await db.query(
      'SELECT * FROM blogs WHERE id = ?',
      [blogId]
    );
    
    if (blogs.length === 0) {
      return res.status(404).json({
        success: false,
        message: 'Không tìm thấy blog'
      });
    }
    
    if (blogs[0].user_id !== userId) {
      return res.status(403).json({
        success: false,
        message: 'Bạn không có quyền xóa blog này'
      });
    }
    
    // Xóa hình ảnh nếu có
    if (blogs[0].image) {
      const imagePath = path.join('uploads', blogs[0].image);
      if (fs.existsSync(imagePath)) {
        fs.unlinkSync(imagePath);
      }
    }
    
    // Xóa blog khỏi database
    await db.query('DELETE FROM blogs WHERE id = ?', [blogId]);
    
    res.json({
      success: true,
      message: 'Xóa blog thành công'
    });
  } catch (error) {
    console.error('Lỗi xóa blog:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi server khi xóa blog'
    });
  }
});

export default router;