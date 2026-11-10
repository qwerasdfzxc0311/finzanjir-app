package uz.finzanjir.nativeoffline;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.Gravity;
import android.view.View;
import android.widget.*;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import java.text.SimpleDateFormat;
import java.util.*;

public class MainActivity extends Activity {
    private DB db;
    private LinearLayout root, body, nav;
    private final int bg = Color.rgb(14,17,23), panel = Color.rgb(30,33,41), green = Color.rgb(76,175,80);
    private String page = "🏦 Sun'iy Bank";
    private final String[] pages = {"🏦 Sun'iy Bank","👨‍💻 Operator Panel","👤 Fuqaro","🌐 Banklararo Tahlil","📊 KPI Dashboard","📜 Audit & 16 Qatlam"};

    @Override public void onCreate(Bundle b) { super.onCreate(b); getWindow().setStatusBarColor(bg); getWindow().setNavigationBarColor(bg); db=new DB(); show(); }
    private TextView text(String s,int size,boolean bold) {
        TextView t=new TextView(this); t.setText(s); t.setTextColor(Color.WHITE); t.setTextSize(size);
        if(bold)t.setTypeface(null,Typeface.BOLD); t.setPadding(12,10,12,10); return t;
    }
    private void addText(String s,int size,boolean bold){ body.addView(text(s,size,bold)); }
    private void button(String s,Runnable r){
        Button b=new Button(this); b.setText(s); b.setAllCaps(false); b.setTextColor(Color.WHITE);
        b.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.rgb(49,85,58)));
        LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,-2); p.setMargins(8,5,8,5); body.addView(b,p);
        b.setOnClickListener(v->r.run());
    }
    private void show(){
        root=new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL); root.setBackgroundColor(bg); setContentView(root);
        TextView header=text("🛡️ FINZANJIR AI  •  v3.2  •  OFFLINE DEMO",18,true); header.setGravity(Gravity.CENTER); root.addView(header);
        HorizontalScrollView hs=new HorizontalScrollView(this); nav=new LinearLayout(this); nav.setOrientation(LinearLayout.HORIZONTAL); hs.addView(nav); root.addView(hs);
        for(String p:pages){ Button n=new Button(this); n.setText(p); n.setTextSize(11); n.setAllCaps(false); nav.addView(n); n.setOnClickListener(v->{page=p;show();}); }
        ScrollView scroll=new ScrollView(this); body=new LinearLayout(this); body.setOrientation(LinearLayout.VERTICAL); body.setPadding(10,8,10,24); scroll.addView(body); root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
        addText(page,22,true); addText("Bu 2-noyabrdagi birinchi FINZANJIR prototipining native Android demo talqini. Haqiqiy bank tizimiga ulanmagan.",13,false);
        if(page.equals(pages[0])) bank(); else if(page.equals(pages[1])) operator(); else if(page.equals(pages[2])) citizen(); else if(page.equals(pages[3])) chain(); else if(page.equals(pages[4])) kpi(); else audit();
    }
    private String joinReasons(ArrayList<String> items){ StringBuilder b=new StringBuilder(); for(String item:items){ if(b.length()>0)b.append(", "); b.append(item); } return b.toString(); }
    private void bank(){
        addText("Sun'iy Bank (L14)",18,true);
        button("➕ 1 ta demo tranzaksiya yaratish",()->{
            Random r=new Random(); int amount=new int[]{50000,150000,2000000,15000000,-500}[r.nextInt(5)];
            String[] devices={"yangi_qurilma","odatiy_qurilma","nomalum_qurilma"};
            String[] places={"Toshkent","Samarqand","Chet_el"};
            String id="TX-"+(10000+r.nextInt(90000)); String device=devices[r.nextInt(3)], place=places[r.nextInt(3)];
            int score=0; ArrayList<String> reasons=new ArrayList<>();
            if(amount<=0){db.save("ERR-"+(1000+r.nextInt(9000)),id,amount,device,place,0,"L02: Xato ma'lumot","CLOSED","ERROR","");db.log("Rad etildi (Sifatsiz): "+id,"L02: Ma'lumot sifati");}
            else {
                if(r.nextDouble()>0.7){score+=30;reasons.add("Tez-tez takrorlanish (Velocity)");}
                if(amount>10000000){score+=40;reasons.add("Katta summa");}
                if(device.equals("nomalum_qurilma")){score+=40;reasons.add("Noma'lum qurilma");}
                if(place.equals("Chet_el")){score+=30;reasons.add("Chet eldan");}
                if(score>=70){String cid="CASE-"+(1000+r.nextInt(9000));db.save(cid,id,amount,device,place,score,joinReasons(reasons),"OPEN","","Karta → Qurilma → Tranzaksiya → Joy");db.log("Case ochildi: "+cid,"L08: Case boshqaruvi");}
                else db.log("O'tdi: "+id,"L07: Avtomatlashtirish");
            }
            show(); addText("Natija: "+id+" | summa: "+amount+" | risk: "+score+"/100",15,true);
            if(amount<=0)addText("Xato ma'lumot (L02) — demo yozuv rad etildi.",14,true);
            else if(score>=70)addText("Case ochildi. Bu avtomatik ayblov yoki bank blokirovkasi emas.",14,true);
            else addText("Tranzaksiya demo qoidalaridan o'tdi.",14,true);
        });
        addText("Risk Engine (L03): 30 — takrorlanish; 40 — katta summa; 40 — noma'lum qurilma; 30 — chet el. Ballar konseptual demo qoidalaridir.",14,false);
    }
    private void caseList(boolean onlyOpen, boolean citizenView){
        Cursor c=db.getReadableDatabase().rawQuery("SELECT case_id,tx_id,amount,device,location,score,reasons,status,decision FROM cases ORDER BY rowid DESC",null);
        if(c.getCount()==0)addText("Hozircha Case yo'q. Sun'iy Bank bo'limida demo tranzaksiya yarating.",14,false);
        while(c.moveToNext()){
            String id=c.getString(0), status=c.getString(7), decision=c.getString(8);
            if(onlyOpen&&!status.equals("OPEN"))continue;
            if(citizenView && !(status.equals("OPEN")||(status.equals("CLOSED")&&"BLOCKED".equals(decision))))continue;
            addText(id+" | Risk: "+c.getInt(5)+"/100 | "+status,17,true);
            addText("Tranzaksiya: "+c.getString(1)+" | Summa: "+c.getInt(2)+" | Qurilma: "+c.getString(3)+" | Joy: "+c.getString(4),13,false);
            addText("Sabab: "+c.getString(6),13,false);
            if(citizenView)addText(status.equals("OPEN")?"Tranzaksiya tekshirilmoqda. Bu shubha signali, ayblov emas.":"Demo holat: bloklangan deb belgilangan. Bankka murojaat qiling.",13,false);
            else if(status.equals("OPEN")){
                button("Operator: demo holatni BLOKLASH deb belgilash",()->{db.update(id,"CLOSED","BLOCKED");db.log("Operator demo qarori: "+id+" BLOCKED","L04: Inson nazorati");show();});
                button("Operator: XAVFSIZ deb belgilash",()->{db.update(id,"CLOSED","SAFE");db.log("Operator demo qarori: "+id+" SAFE","L04: Inson nazorati");show();});
            }
        } c.close();
    }
    private void operator(){addText("Operator Panel (L04) — inson nazorati",17,true);caseList(true,false);}
    private void citizen(){addText("Fuqaro (L09) — faqat demo holatlar",17,true);caseList(false,true);}
    private void chain(){addText("Banklararo Integratsiya (L14)",18,true);button("🔄 Zanjirni simulyatsiya qilish",()->{addText("A Bank (Fuqaro)  →  B Bank (Vositachi)  →  C Bank (Vositachi)  →  D Bank (Naqd)",15,true);addText("⚠️ Demo ssenariy: mablag' bir nechta bank orqali o'tib naqdlashtirilgan (Money Mule).",14,false);});}
    private void kpi(){
        Cursor c=db.getReadableDatabase().rawQuery("SELECT COUNT(*),SUM(CASE WHEN decision='BLOCKED' THEN 1 ELSE 0 END),SUM(CASE WHEN decision='SAFE' THEN 1 ELSE 0 END),SUM(CASE WHEN decision='ERROR' THEN 1 ELSE 0 END),SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END) FROM cases",null);
        if(c.moveToFirst()){addText("Jami Case/yozuv: "+c.getInt(0),18,true);addText("Tekshirilmoqda: "+c.getInt(4),16,false);addText("Demo bloklangan: "+c.getInt(1),16,false);addText("Xavfsiz deb belgilangan: "+c.getInt(2),16,false);addText("Xato ma'lumot: "+c.getInt(3),16,false);} c.close();
        addText("Ko'rsatkichlar faqat ushbu telefondagi demo bazadan hisoblanadi.",13,false);
    }
    private void audit(){addText("Audit Jurnali (L13)",18,true);Cursor c=db.getReadableDatabase().rawQuery("SELECT time,layer,message FROM audit_log ORDER BY id DESC LIMIT 50",null);while(c.moveToNext())addText("["+c.getString(0)+"] ["+c.getString(1)+"] "+c.getString(2),13,false);c.close();
        addText("16 qatlam statusi — boshlang'ich Streamlit prototipidagi ta'riflar:",16,true);
        String[] layers={"L01 Dalil va Manba","L02 Ma'lumot Sifati","L03 Xavf Baholash","L04 Inson Nazorati","L05 Qoidalar Boshqaruvi","L06 Maxfiylik","L07 Avtomatlashtirish","L08 Case Boshqaruvi","L09 Fuqaro Shaffofligi","L10 Hayotiy Sikl","L11 Hodisaga Javob","L12 AI Ishonchliligi","L13 Audit","L14 Bank Integratsiyasi","L15 Yuklama","L16 Ta'sir (KPI)"};
        for(String l:layers)addText(l+" — demo darajasida",13,false);
    }
    private class DB extends SQLiteOpenHelper {
        DB(){super(MainActivity.this,"finzanjir.db",null,1);}
        public void onCreate(SQLiteDatabase d){d.execSQL("CREATE TABLE cases(case_id TEXT PRIMARY KEY,tx_id TEXT,amount INTEGER,device TEXT,location TEXT,score INTEGER,reasons TEXT,status TEXT,decision TEXT,graph_data TEXT)");d.execSQL("CREATE TABLE audit_log(id INTEGER PRIMARY KEY AUTOINCREMENT,time TEXT,layer TEXT,message TEXT)");}
        public void onUpgrade(SQLiteDatabase d,int a,int b){}
        void save(String id,String tx,int amount,String device,String loc,int score,String reasons,String status,String decision,String graph){android.content.ContentValues v=new android.content.ContentValues();v.put("case_id",id);v.put("tx_id",tx);v.put("amount",amount);v.put("device",device);v.put("location",loc);v.put("score",score);v.put("reasons",reasons);v.put("status",status);v.put("decision",decision);v.put("graph_data",graph);getWritableDatabase().insertWithOnConflict("cases",null,v,SQLiteDatabase.CONFLICT_REPLACE);}
        void update(String id,String status,String decision){android.content.ContentValues v=new android.content.ContentValues();v.put("status",status);v.put("decision",decision);getWritableDatabase().update("cases",v,"case_id=?",new String[]{id});}
        void log(String msg,String layer){String now=new SimpleDateFormat("HH:mm:ss",Locale.US).format(new Date());android.content.ContentValues v=new android.content.ContentValues();v.put("time",now);v.put("layer",layer);v.put("message",msg);getWritableDatabase().insert("audit_log",null,v);}
    }
}
