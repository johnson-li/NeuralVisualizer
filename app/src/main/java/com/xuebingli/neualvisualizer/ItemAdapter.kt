package com.xuebingli.neualvisualizer

import android.support.v7.app.AlertDialog
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import com.pixplicity.easyprefs.library.Prefs

class ItemAdapter : RecyclerView.Adapter<ItemViewHolder>() {

    val items = arrayOf(Item("Label number", Cons.LABEL_NUMBER),
            Item("Image number", Cons.IMAGE_NUMBER), Item("Show labels", Cons.SHOW_LABEL),
            Item("Iteration", Cons.ITERATION))

    override fun onCreateViewHolder(p0: ViewGroup, p1: Int): ItemViewHolder {
        val view = LayoutInflater.from(p0.context).inflate(R.layout.item_view, p0, false)
        return ItemViewHolder(view)
    }

    override fun getItemCount(): Int {
        return items.size
    }

    override fun onBindViewHolder(p0: ItemViewHolder, p1: Int) {
        val title = p0.itemView.findViewById<TextView>(R.id.title)
        val content = p0.itemView.findViewById<TextView>(R.id.content)
        title.text = items[p1].title
        when (p1) {
            0 -> {
                content.text = Prefs.getInt(Cons.LABEL_NUMBER, 10).toString()
                p0.itemView.rootView.setOnClickListener {
                    AlertDialog.Builder(p0.itemView.context).setItems(arrayOf("2", "3", "4", "5", "6", "7", "8", "9", "10"), { dialog, which ->
                        Prefs.putInt(Cons.LABEL_NUMBER, which + 2)
                        notifyItemChanged(p1)
                    }).setTitle(title.text).create().show()
                }
            }
            1 -> {
                content.text = Prefs.getInt(Cons.IMAGE_NUMBER, 100).toString()
                val numbers = arrayOf("10", "50", "100", "200", "400")
                p0.itemView.rootView.setOnClickListener {
                    AlertDialog.Builder(p0.itemView.context).setItems(numbers, { dialog, which ->
                        Prefs.putInt(Cons.IMAGE_NUMBER, numbers[which].toInt())
                        notifyItemChanged(p1)
                    }).setTitle(title.text).create().show()
                }
            }
            2 -> {
                content.text = Prefs.getBoolean(Cons.SHOW_LABEL, true).toString()
                val choices = arrayOf("true", "false")
                p0.itemView.rootView.setOnClickListener {
                    AlertDialog.Builder(p0.itemView.context).setItems(choices, { dialog, which ->
                        Prefs.putBoolean(Cons.SHOW_LABEL, choices[which].toBoolean())
                        notifyItemChanged(p1)
                    }).setTitle(title.text).create().show()
                }
            }
            3 -> {
                content.text = Prefs.getInt(Cons.ITERATION, 1000).toString()
                val choices = arrayOf("500", "1000", "2000", "4000")
                p0.itemView.rootView.setOnClickListener {
                    AlertDialog.Builder(p0.itemView.context).setItems(choices, { dialog, which ->
                        Prefs.putInt(Cons.ITERATION, choices[which].toInt())
                        notifyItemChanged(p1)
                    }).setTitle(title.text).create().show()
                }
            }
        }
    }
}

class Item(val title: String, val key: String)

class ItemViewHolder(view: View) : RecyclerView.ViewHolder(view)